from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_user.services import RoleService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from api_user.models import Role
from api_user.serializers import RoleSerializer
from common.constants.base import ErrorResponse, ErrorResponseType


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.exclude(name__exact="Super Administrator")
    serializer_class = RoleSerializer
    permission_classes = [MyActionPermission]
    required_alternate_scopes = {
        "list": ["role:view"],
        "retrieve": ["role:view"],
        "update": ["role:edit"],
        "create": ["role:edit"]
    }

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.initial_data.update({"last_modified_by": request.user.profile.name})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.initial_data.update({"last_modified_by": request.user.profile.name})
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                new_role = Role.objects.by_name(data.get("name"))
                RoleService.mock_default_scope(new_role)
                serializer = self.get_serializer(Role.objects.by_name(data.get("name")))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["role"])
