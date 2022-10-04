from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_user.models.profile import Profile
from api_user.serializers import ProfileSerializer, ProfileDetailSerializer
from api_user.services import ProfileService
from api_user.statics import RoleData
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import HttpMethod, ErrorResponse, ErrorResponseType


class ProfileViewSet(BaseViewSet):
    view_set_name = "profile"
    queryset = Profile.objects.active().all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [MyActionPermission]
    required_alternate_scopes = {
        "retrieve": ["user:view_ger_info"],
        "update": ["user:edit_private_info", "user:edit_public_inf", "employee:edit_employee_info"],
        "get_list_employee": ['employee:view_employee_info']
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_list_employee(self, request, *arg, **kwargs):
        queryset = self.get_queryset().filter(account__roles__in=[RoleData.EMPLOYEE.value.get('id')])
        queryset = ProfileService.get_filter_query(request, queryset)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            account = instance.account
            if account:
                account.active = False
                account.save()
            else:
                self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            ErrorResponse(ErrorResponseType.CANT_DEACTIVATE, params=["profile"])
