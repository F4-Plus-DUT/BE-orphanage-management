from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_user.models.profile import Profile
from api_user.serializers import ProfileDetailSerializer, ProfileSerializer
from api_user.services import ProfileService, RoleService
from api_user.statics import RoleData
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import HttpMethod, ErrorResponse, ErrorResponseType
from utils import gen_password


class ProfileViewSet(BaseViewSet):
    view_set_name = "profile"
    queryset = Profile.objects.active().all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [MyActionPermission]
    serializer_map = {
        "create_employee": ProfileSerializer,
    }
    required_alternate_scopes = {
        "retrieve": ["user:view_ger_info"],
        "update": ["user:edit_private_info", "user:edit_public_inf", "employee:edit_employee_info"],
        "get_list_employee": ['employee:view_employee_info'],
        "create_employee": ["user:edit_private_info", "user:edit_public_inf", "employee:edit_employee_info"],
        "create": ["user:edit_private_info", "user:edit_public_inf", "employee:edit_employee_info"],
        "destroy": ["user:edit_private_info", "user:edit_public_inf", "employee:edit_employee_info"],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_list_employee(self, request, *arg, **kwargs):
        queryset = self.get_queryset().filter(account__roles__in=[RoleData.EMPLOYEE.value.get('id')])
        queryset = ProfileService.get_filter_query(request, queryset)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(methods=[HttpMethod.POST], detail=False)
    def create_employee(self, request, *args, **kwargs):
        data = request.data
        data["password"] = gen_password()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                user = ProfileService.create_profile(
                    RoleService.get_role_employee(), serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["profile"])

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=ProfileService.init_data_profile(request, instance))
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_update(serializer)
                if getattr(instance, "_prefetched_objects_cache", None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return ErrorResponse(ErrorResponseType.CANT_UPDATE, params=["profile"])

