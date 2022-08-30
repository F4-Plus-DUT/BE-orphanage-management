from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api_base.consts import ScopeAction


class BaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    permission_map = {}
    view_set_name = "base"
    base_scopes = {
        ScopeAction.VIEW: f"{view_set_name}::{ScopeAction.VIEW.value}",
        ScopeAction.EDIT: f"{view_set_name}::{ScopeAction.EDIT.value}",
        ScopeAction.FULL: f"{view_set_name}::{ScopeAction.FULL.value}",
    }
    scope_mapper = {
        "list": [base_scopes[ScopeAction.VIEW]],
        "retrieve": [base_scopes[ScopeAction.VIEW]],
        "create": [base_scopes[ScopeAction.EDIT]],
        "update": [base_scopes[ScopeAction.EDIT]],
        "partial_update": [base_scopes[ScopeAction.EDIT]],
        "destroy": [base_scopes[ScopeAction.FULL]],
    }
    endpoint_descriptions = {}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission_map.get(self.action, self.permission_classes)]

    @action(detail=True, methods=['put'])
    def deactivate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_activate = False
        account = getattr(instance, 'account', None)
        if account:
            account.is_activate = False
            account.save()
        instance.save()
        return Response({"details": "deactivated"})

    @action(detail=True, methods=['put'])
    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_activate = True
        instance.save()
        account = getattr(instance, 'account', None)
        if account:
            account.is_activate = True
            account.save()
        return Response({"details": "activated"})
