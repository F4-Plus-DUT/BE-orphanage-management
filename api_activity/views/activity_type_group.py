from api_activity.models import ActivityTypeGroup
from api_activity.serializers import ActivityTypeGroupSerializer
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet


class ActivityTypeGroupViewSet(BaseViewSet):
    view_set_name = "activity_type_group"
    queryset = ActivityTypeGroup.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = ActivityTypeGroupSerializer
    pagination_class = None
    required_alternate_scopes = {
        "list": [],
    }

