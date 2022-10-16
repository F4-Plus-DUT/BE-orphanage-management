from rest_framework import status
from rest_framework.response import Response

from api_activity.models import ActivityType
from api_activity.serializers import ActivityTypeSerializer
from api_activity.services.activity_type import ActivityTypeService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet


class ActivityTypeViewSet(BaseViewSet):
    view_set_name = "activity_type"
    queryset = ActivityType.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = ActivityTypeSerializer
    pagination_class = None
    required_alternate_scopes = {
        "list": ["activity:view_activity"],
    }

    def list(self, request, *args, **kwargs):
        queryset = ActivityTypeService.get_filter_query(request)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
