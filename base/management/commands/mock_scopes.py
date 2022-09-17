from api_user.models import Role
from api_user.statics import RoleData
from api_user.utils import split_scopes, get_default_scopes, concat_scopes
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
            default_scopes = set(split_scopes(get_default_scopes()))
            roles = Role.objects.all().exclude(id=RoleData.ADMIN.value.get('id'))
            for role in roles:
                scopes = set(split_scopes(role.scope_text))
                new_default_scopes = default_scopes.difference(scopes)

                scopes = scopes.union(new_default_scopes) if new_default_scopes else scopes

                role.scope_text = concat_scopes(list(scopes))
                role.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
