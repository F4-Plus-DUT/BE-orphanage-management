from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from base.consts import ScopeAction, Flag, ErrorResponse, ErrorResponseType
from base.utils.model import ModelUtils


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
        is_success = ModelUtils.active_instance(instance, Flag.OFF)
        if is_success:
            return Response({"details": "deactivated"})
        else:
            return ErrorResponse(ErrorResponseType.CANT_DEACTIVATE, params=[f"{ModelUtils.get_model_name(instance)} with id: {instance.pk}"])

    @action(detail=True, methods=['put'])
    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        is_success = ModelUtils.active_instance(instance, Flag.ON)
        if is_success:
            return Response({"details": "activated"})
        else:
            return ErrorResponse(
                ErrorResponseType.CANT_ACTIVATE,
                params=[f"{ModelUtils.get_model_name(instance)} with id: {instance.pk}"]
            )
