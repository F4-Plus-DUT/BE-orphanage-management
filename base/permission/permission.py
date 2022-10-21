from rest_framework.permissions import BasePermission

from api_user.statics import RoleData
from core.settings import SCOPES


class MyActionPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        required_alternate_scopes = getattr(view, "required_alternate_scopes")
        action = view.action.lower()

        if action in required_alternate_scopes:
            if len(required_alternate_scopes[action]) == 0:
                return True

        if not token:
            return False

        user_roles = request.user.roles
        user_scopes = self.get_scopes_user_role(user_roles)

        if action in required_alternate_scopes:
            return any(
                scope in user_scopes for scope in required_alternate_scopes[action]
            )
        else:
            return True

    @classmethod
    def get_scopes_user_role(cls, roles):
        user_scopes = list()
        if roles:
            for role in roles.all():
                scope_text = role.scope_text
                if role.name == RoleData.ADMIN.value.get('name'):
                    return list(SCOPES.keys())
                for scope in scope_text.split(' '):
                    user_scopes.append(scope.strip())
        return user_scopes
