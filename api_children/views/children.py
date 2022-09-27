from api_children.models import Children
from api_children.serializers import ChildrenSerializer
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet


class ChildrenViewSet(BaseViewSet):
    view_set_name = "children"
    queryset = Children.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = ChildrenSerializer
    required_alternate_scopes = {
        "retrieve": ["children:view_children_info"],
        "list": ["children:view_children_info"],
        "update": ["children:edit_children_info"],
    }
