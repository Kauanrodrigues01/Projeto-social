from django.db import models
from django.utils import timezone


class Payment(models.Model):
    TIPO_DOACAO_CHOICES = [
        ("brinquedos", "Brinquedos"),
        ("alimentacao", "Alimentação"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("approved", "Aprovado"),
        ("rejected", "Rejeitado"),
        ("cancelled", "Cancelado"),
    ]

    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    data = models.DateTimeField(default=timezone.now, verbose_name="Data")
    payment_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID do Pagamento"
    )
    payment_url = models.URLField(
        blank=True, null=True, verbose_name="URL do Pagamento"
    )
    qr_code = models.TextField(
        blank=True, null=True, verbose_name="QR Code PIX (texto)"
    )
    qr_code_base64 = models.TextField(
        blank=True, null=True, verbose_name="QR Code PIX (Base64)"
    )
    tipo_doacao = models.CharField(
        max_length=20,
        choices=TIPO_DOACAO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tipo de Doação",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status"
    )
    nome_doador = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Nome do Doador"
    )
    email_doador = models.EmailField(
        blank=True, null=True, verbose_name="Email do Doador"
    )

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ["-data"]

    def __str__(self):
        tipo = self.get_tipo_doacao_display() if self.tipo_doacao else "Geral"
        return f"Doação de R$ {self.valor} - {tipo} - {self.data.strftime('%d/%m/%Y')}"
