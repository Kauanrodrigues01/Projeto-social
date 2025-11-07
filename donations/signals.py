from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """Cria um superusuário automaticamente após as migrações"""
    if sender.name == "donations":  # Executa apenas na primeira vez
        User = get_user_model()

        username = settings.SUPERUSER_EMAIL  # Usa o email como username
        password = settings.SUPERUSER_PASSWORD

        if (
            username
            and password
            and not User.objects.filter(username=username).exists()
        ):
            User.objects.create_superuser(
                username=username,
                email="",  # Email vazio
                password=password,
            )
            print(f"✅ Superusuário criado: {username}")
