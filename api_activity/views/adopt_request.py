from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_activity.models import AdoptRequest
from api_activity.serializers import AdoptRequestSerializer
from api_activity.services import AdoptRequestService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType


class AdoptRequestViewSet(BaseViewSet):
    view_set_name = "adopt_request"
    queryset = AdoptRequest.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = AdoptRequestSerializer
    required_alternate_scopes = {
        "retrieve": ["adopt_request:view_adopt_request"],
        "list": ["adopt_request:view_adopt_request"],
        "create": ["adopt_request:create_adopt_request"],
        "update": ["adopt_request:update_adopt_request"],
    }

    def create(self, request, *args, **kwargs):
        serializer = AdoptRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                AdoptRequestService.send_notify(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["adopt_request"])
