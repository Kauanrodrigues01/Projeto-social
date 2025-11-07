from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from services.mercadopago import MercadoPagoService

from .models import Payment


def donation_page(request):
    """Página de doação onde o usuário escolhe o valor e tipo de doação"""
    if request.method == "POST":
        valor = request.POST.get("valor")
        nome_doador = request.POST.get("nome_doador")

        # Tipo de doação agora é sempre brinquedos
        tipo_doacao = "brinquedos"

        # Validações
        if not valor:
            messages.error(request, "Por favor, informe o valor da doação.")
            return render(request, "donations/donation_page.html")

        try:
            valor = float(valor)
            if valor < 0.01:
                messages.error(request, "O valor mínimo é R$ 0,01.")
                return render(request, "donations/donation_page.html")
        except ValueError:
            messages.error(request, "Valor inválido.")
            return render(request, "donations/donation_page.html")

        # Criar pagamento no banco de dados
        payment = Payment.objects.create(
            valor=valor,
            tipo_doacao=tipo_doacao,
            nome_doador=nome_doador if nome_doador else None,
            status="pending",
        )

        # Criar pagamento PIX no Mercado Pago
        try:
            # Preparar descrição do pagamento
            descricao = "Doação ToyLink - Brinquedos"

            # Criar pagamento PIX
            mp_service = MercadoPagoService()
            mp_response = mp_service.pay_with_pix(
                amount=float(valor),
                payer_email="doacao@example.com",
                payer_cpf="00000000000",
                description=descricao,
            )

            # Atualizar payment com dados do Mercado Pago
            payment.payment_id = str(mp_response.get("id"))
            payment.payment_url = (
                mp_response.get("point_of_interaction", {})
                .get("transaction_data", {})
                .get("ticket_url")
            )
            payment.qr_code = (
                mp_response.get("point_of_interaction", {})
                .get("transaction_data", {})
                .get("qr_code")
            )
            payment.qr_code_base64 = (
                mp_response.get("point_of_interaction", {})
                .get("transaction_data", {})
                .get("qr_code_base64")
            )
            payment.save()

            messages.success(request, "Pagamento PIX gerado com sucesso!")

        except Exception as e:
            # Se falhar ao criar no Mercado Pago, manter pagamento local
            messages.warning(
                request, f"Doação registrada, mas houve um erro ao gerar PIX: {str(e)}"
            )

        return redirect("waiting_payment", payment_id=payment.id)

    return render(request, "donations/donation_page.html")


def waiting_payment(request, payment_id):
    """Página de aguardando pagamento com QR code e opção de verificar status"""
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == "POST":
        # Verificar status no Mercado Pago
        if payment.payment_id:
            try:
                mp_service = MercadoPagoService()
                payment_info = mp_service.get_payment_info(payment.payment_id)

                # Atualizar status do pagamento
                mp_status = payment_info.get("status")

                if mp_status == "approved":
                    payment.status = "approved"
                    if not payment.data:
                        from datetime import datetime

                        payment.data = datetime.now()
                    payment.save()
                    messages.success(
                        request, "Pagamento aprovado! Obrigado pela sua doação! 🎉"
                    )
                elif mp_status == "pending":
                    messages.info(
                        request,
                        "Pagamento ainda não foi confirmado. Aguarde alguns instantes.",
                    )
                elif mp_status == "rejected":
                    payment.status = "rejected"
                    payment.save()
                    messages.error(request, "Pagamento foi recusado.")
                elif mp_status == "cancelled":
                    payment.status = "cancelled"
                    payment.save()
                    messages.warning(request, "Pagamento foi cancelado.")
                else:
                    messages.warning(request, f"Status do pagamento: {mp_status}")

            except Exception as e:
                messages.error(request, f"Erro ao verificar status: {str(e)}")
        else:
            # Fallback para quando não tem payment_id do MP
            if payment.status == "pending":
                messages.info(
                    request,
                    "Pagamento ainda não foi confirmado. Aguarde alguns instantes.",
                )
            elif payment.status == "approved":
                messages.success(
                    request, "Pagamento aprovado! Obrigado pela sua doação!"
                )
            else:
                messages.warning(
                    request, f"Status do pagamento: {payment.get_status_display()}"
                )

        # Redirecionar para evitar reenvio de formulário ao recarregar
        return redirect("waiting_payment", payment_id=payment.id)

    context = {
        "payment": payment,
    }
    return render(request, "donations/waiting_payment.html", context)


@login_required
def dashboard(request):
    """Dashboard administrativo para visualizar doações"""
    payments = Payment.objects.all().order_by("-data")

    # Estatísticas
    total_arrecadado = sum(p.valor for p in payments if p.status == "approved")
    total_pendente = sum(p.valor for p in payments if p.status == "pending")
    total_doacoes = payments.filter(status="approved").count()

    # Filtros
    status_filter = request.GET.get("status")

    if status_filter:
        payments = payments.filter(status=status_filter)

    # Paginação
    paginator = Paginator(payments, 20)  # 20 doações por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "payments": page_obj,  # Mantém compatibilidade com o template
        "total_arrecadado": total_arrecadado,
        "total_pendente": total_pendente,
        "total_doacoes": total_doacoes,
        "status_filter": status_filter,
    }
    return render(request, "donations/dashboard.html", context)
