from api_activity.models import Activity
from api_activity.serializers import ActivitySerializer
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet


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
