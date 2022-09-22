from rest_framework.decorators import action

from api_children.models import Children
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import HttpMethod


class ProfileViewSet(BaseViewSet):
    view_set_name = "children"
    queryset = Children.objects.all()
    permission_classes = [MyActionPermission]
    required_alternate_scopes = {
        "retrieve": ["children:view_children_info"],
        "list": ["children:view_children_info"],
        "update": ["children:edit_children_info"],
    }