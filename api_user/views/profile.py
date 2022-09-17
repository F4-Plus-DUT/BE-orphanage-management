from rest_framework.decorators import action

from api_user.models.profile import Profile
from api_user.serializers import ProfileSerializer, ProfileDetailSerializer
from api_user.statics import RoleData
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import HttpMethod


class ProfileViewSet(BaseViewSet):
    view_set_name = "profile"
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [MyActionPermission]
    required_alternate_scopes = {
        "retrieve": ["user:view_ger_info"]
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_list_employee(self, request, *arg, **kwargs):
        queryset = self.get_queryset().filter(account__roles__in=[RoleData.EMPLOYEE.value.get('id')])
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)
