import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Aguarda o banco de dados estar disponível"

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Tempo máximo de espera em segundos (padrão: 30)",
        )

    def handle(self, *args, **options):
        timeout = options["timeout"]
        self.stdout.write("⏳ Aguardando banco de dados...")

        db_conn = None
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS("✅ Banco de dados disponível!"))
                return
            except OperationalError:
                elapsed = int(time.time() - start_time)
                self.stdout.write(
                    f"⏳ Banco de dados indisponível. Aguardando... ({elapsed}s/{timeout}s)"
                )
                time.sleep(1)

        self.stdout.write(
            self.style.ERROR(
                f"❌ Timeout: Banco de dados não ficou disponível em {timeout} segundos"
            )
        )
        raise OperationalError(
            f"Database did not become available within {timeout} seconds"
        )
