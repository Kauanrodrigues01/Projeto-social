from django.urls import path

from . import views

urlpatterns = [
    path("webhook/mercadopago/", views.webhook_mercadopago, name="webhook_mercadopago"),
]
