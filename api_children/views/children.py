from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_children.models import Children
from api_children.serializers import ChildrenSerializer
from api_children.services import ChildrenService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType


class ChildrenViewSet(BaseViewSet):
    view_set_name = "children"
    queryset = Children.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = ChildrenSerializer
    required_alternate_scopes = {
        "retrieve": ["children:view_children_info"],
        "list": ["children:view_children_info"],
        "update": ["children:edit_children_info"],
        "create": ["children:view_children_info"],
        "destroy": ["children:view_children_info"],
    }

    def list(self, request, *args, **kwargs):
        queryset = ChildrenService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=ChildrenService.init_data_children(request))
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["children"])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=ChildrenService.init_data_children(request))
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_update(serializer)
                if getattr(instance, "_prefetched_objects_cache", None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return ErrorResponse(ErrorResponseType.CANT_UPDATE, params=["children"])
