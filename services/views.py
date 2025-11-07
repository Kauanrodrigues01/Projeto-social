import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from donations.models import Payment

from .mercadopago import MercadoPagoService


def update_payment_status(
    payment_id: str,
    status: str,
    status_detail: str,
    date_approved: str = None,
    external_reference: str = None,
) -> dict:
    """
    Atualiza o status de um pagamento no banco de dados.

    Args:
        payment_id: ID do pagamento no Mercado Pago
        status: Status do pagamento (approved, pending, rejected, etc.)
        status_detail: Detalhe do status
        date_approved: Data de aprovação do pagamento
        external_reference: Referência externa (opcional)

    Returns:
        dict: {"success": bool, "message": str, "payment": Payment}
    """
    try:
        # Buscar pagamento pelo payment_id do Mercado Pago
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return {
                "success": False,
                "message": f"Pagamento com payment_id {payment_id} não encontrado",
                "payment": None,
            }

        # Mapear status do Mercado Pago para status do sistema
        status_mapping = {
            "approved": "approved",
            "pending": "pending",
            "in_process": "pending",
            "rejected": "rejected",
            "cancelled": "cancelled",
            "refunded": "cancelled",
            "charged_back": "cancelled",
        }

        new_status = status_mapping.get(status, "pending")
        old_status = payment.status

        # Atualizar status do pagamento
        payment.status = new_status

        # Se foi aprovado, registrar a data de aprovação
        if new_status == "approved" and date_approved:
            try:
                from datetime import datetime

                payment.data = datetime.fromisoformat(
                    date_approved.replace("Z", "+00:00")
                )
            except Exception:
                pass  # Manter a data original se houver erro

        payment.save()

        message = f"Pagamento #{payment.id} atualizado: {old_status} → {new_status}"

        # Log adicional se foi aprovado
        if new_status == "approved":
            message += f" | Doação de R$ {payment.valor} confirmada!"

        return {
            "success": True,
            "message": message,
            "payment": payment,
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao atualizar pagamento: {str(e)}",
            "payment": None,
        }


@csrf_exempt
def webhook_mercadopago(request):
    """
    Webhook do MercadoPago para processar atualizações de pagamento.
    Suporta tanto o formato antigo (action/data) quanto o novo (resource/topic).
    """
    if request.method != "POST":
        return HttpResponse(status=405)  # Method Not Allowed

    try:
        # Parse do JSON recebido
        data = json.loads(request.body.decode("utf-8"))
        print(f"🔔 Webhook MercadoPago recebido: {data}")
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    # Verificar formato do webhook
    payment_id = None

    # Novo formato: {"resource":"125381511429","topic":"payment"}
    if "topic" in data and "resource" in data:
        topic = data.get("topic")
        if topic != "payment":
            return HttpResponse("Topic not supported", status=200)
        payment_id = data.get("resource")

    # Formato antigo: {"action":"payment.updated","data":{"id":"123"}}
    elif "action" in data and "data" in data:
        action = data.get("action")
        if action != "payment.updated":
            return HttpResponse("Action not supported", status=200)
        payment_id = data.get("data", {}).get("id")

    else:
        return HttpResponse("Invalid webhook format", status=400)

    if not payment_id:
        return HttpResponse("No payment ID", status=400)

    try:
        # Buscar detalhes do pagamento no MercadoPago
        mercado_pago = MercadoPagoService()
        payment_data = mercado_pago.get_payment_info(payment_id)

        if not payment_data:
            return HttpResponse("Payment not found", status=404)

        # Extrair informações do pagamento
        status = payment_data.get("status")
        status_detail = payment_data.get("status_detail")
        date_approved = payment_data.get("date_approved")
        external_reference = payment_data.get("external_reference")

        # Log da operação (para debug)
        print(
            f"💰 Webhook MercadoPago - Payment ID: {payment_id}, "
            f"Status: {status}/{status_detail}, "
            f"External Ref: {external_reference}"
        )

        # Atualizar status do pagamento
        update_result = update_payment_status(
            payment_id=str(payment_id),
            status=status,
            status_detail=status_detail,
            date_approved=date_approved,
            external_reference=external_reference,
        )

        if not update_result["success"]:
            print(f"❌ Erro ao atualizar pagamento: {update_result['message']}")
            return HttpResponse(update_result["message"], status=400)

        print(f"✅ Webhook processado com sucesso: {update_result['message']}")
        return HttpResponse("OK", status=200)

    except Exception as e:
        print(f"❌ Erro no webhook MercadoPago: {str(e)}")
        return HttpResponse(f"Internal error: {str(e)}", status=500)
