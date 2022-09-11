from api_user.models import Role
from core.settings import DEFAULT_SCOPES
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create mock data"

    def handle(self, *args, **kwargs):
        """
        Insert mock data
        """
        try:
            # Role
            Role.objects.get_or_create(
                name="Customer",
                description="Customer of F4plus orphanage",
                scope_text=" ".join(DEFAULT_SCOPES.keys()),
            )
            Role.objects.get_or_create(
                name="Employee",
                description="Employee of F4plus orphanage",
                scope_text=" ".join(DEFAULT_SCOPES.keys()),
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
