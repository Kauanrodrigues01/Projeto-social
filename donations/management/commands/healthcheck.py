from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Verifica se a aplicação está saudável (healthcheck)"

    def handle(self, *args, **options):
        try:
            # Verifica conexão com o banco de dados
            connection.ensure_connection()

            # Pode adicionar outras verificações aqui
            # Por exemplo: cache, serviços externos, etc.

            self.stdout.write(self.style.SUCCESS("✅ Healthy"))
            return
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"❌ Unhealthy: {str(e)}"))
            exit(1)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
            exit(1)
