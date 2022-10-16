from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_activity.models import Activity
from api_activity.serializers import ActivitySerializer
from api_activity.services.activity import ActivityService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType


class ActivityViewSet(BaseViewSet):
    view_set_name = "activity"
    queryset = Activity.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = ActivitySerializer
    required_alternate_scopes = {
        "retrieve": ["activity:view_activity"],
        "list": ["activity:view_activity"],
        "create": ["activity:edit_activity"],
        "update": ["activity:edit_activity"],
    }

    def list(self, request, *args, **kwargs):
        queryset = ActivityService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=ActivityService.init_data_activity(request))
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                ActivityService.send_notify(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["activity"])
