from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.constants.base import Flag, ErrorResponse, ErrorResponseType
from base.utils.model import ModelUtils


class BaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    permission_map = {}
    view_set_name = "base"

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
