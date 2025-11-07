from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria um superusuário automaticamente se não existir"

    def handle(self, *args, **options):
        User = get_user_model()

        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD

        if not User.objects.filter(username="admin").exists():
            self.stdout.write(self.style.WARNING("Criando superusuário..."))
            User.objects.create_superuser(
                username="admin", email=email, password=password
            )
            self.stdout.write(self.style.SUCCESS("✅ Superusuário criado com sucesso!"))
            self.stdout.write(self.style.SUCCESS("   Username: admin"))
            self.stdout.write(self.style.SUCCESS(f"   Email: {email}"))
            self.stdout.write(self.style.WARNING(f"   Senha: {password}"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ Superusuário já existe"))
