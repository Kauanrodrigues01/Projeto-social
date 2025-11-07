from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "valor", "tipo_doacao", "status", "nome_doador", "data"]
    list_filter = ["status", "tipo_doacao", "data"]
    search_fields = ["nome_doador", "email_doador", "payment_id"]
    readonly_fields = ["data"]
    list_per_page = 20

    fieldsets = (
        ("Informações da Doação", {"fields": ("valor", "tipo_doacao", "status")}),
        ("Dados do Doador", {"fields": ("nome_doador", "email_doador")}),
        ("Informações do Pagamento", {"fields": ("payment_id", "payment_url", "data")}),
    )
