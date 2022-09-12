import logging

from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission

from api_user.statics import RoleData
from core.settings import SCOPES, DEFAULT_SCOPES


class MyActionPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        user_roles = request.user.roles
        user_scopes = self.get_scopes_user_role(user_roles)

        if not token:
            return False

        required_alternate_scopes = getattr(view, "required_alternate_scopes")
        action = view.action.lower()
        if action in required_alternate_scopes:
            return any(
                scope in user_scopes for scope in required_alternate_scopes[action]
            )
        else:
            return True

    @classmethod
    def get_scopes_user_role(cls, roles):
        user_scopes = []
        if roles:
            for role in roles.all():
                scope_text = role.scope_text
                if role.id == RoleData.ADMIN.value.get('id'):
                    return [SCOPES.keys()]
                if role.id == RoleData.CUSTOMER.value.get('id'):
                    return [DEFAULT_SCOPES.keys()]
                user_scopes.append(scope for scope in scope_text.split(' '))
        return user_scopes
