import os

from django.contrib.auth.hashers import make_password, check_password
from requests import Response
from rest_framework import status
from rest_framework.decorators import action

from api_user.models import Account
from api_user.serializers import AccountSerializer
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import HttpMethod


class AccountViewSet(BaseViewSet):
    view_set_name = "account"
    queryset = Account.objects.select_related("profile").prefetch_related("roles")
    permission_classes = [MyActionPermission]
    serializer_class = AccountSerializer
    required_alternate_scopes = {
        "list": ["user:view_ger_info"],
        "retrieve": ["user:view_ger_info"],
        "reset_password": ["admin:reset_password"],
        "change_password": ["user:edit_pub_info"]
    }

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(detail=False, methods=['patch'])
    def change_password(self, request, *args, **kwargs):
        account = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if check_password(old_password, account.password):
            account.password = make_password(new_password)
            account.save()
            return Response({"detail": "Changed password!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error_message": "Old password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=HttpMethod.PUT, detail=True)
    def reset_password(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.password = make_password(os.getenv('DEFAULT_PASSWORD'))
            instance.save()
            return Response({"success": "Reset password!"}, status=status.HTTP_200_OK)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)
