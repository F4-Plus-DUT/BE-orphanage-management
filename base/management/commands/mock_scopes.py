from api_user.models import Role
from api_user.services import RoleService
from api_user.statics import RoleData
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Mock scopes"

    def handle(self, *args, **kwargs):
        """
        Insert scopes for role
        Run: python3 manage.py mock_scopes
        """
        try:
            # Mock default_scopes for all roles except Admin
            roles = Role.objects.all().exclude(id=RoleData.ADMIN.value.get('id'))
            for role in roles:
                RoleService.mock_default_scope(role)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
