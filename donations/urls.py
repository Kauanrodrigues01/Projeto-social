from django.urls import path

from . import views

urlpatterns = [
    path("", views.donation_page, name="donation_page"),
    path("aguardando/<int:payment_id>/", views.waiting_payment, name="waiting_payment"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
