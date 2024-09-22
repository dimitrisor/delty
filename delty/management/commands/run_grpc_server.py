from django.core.management.base import BaseCommand
from delty.grpc.server import serve


class Command(BaseCommand):
    help = "Runs the gRPC server"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting gRPC server..."))
        serve()
