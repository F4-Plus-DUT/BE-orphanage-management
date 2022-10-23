import os

from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_user.models import Account
from api_user.serializers import AccountSerializer
from api_user.services import ProfileService, AccountService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import HttpMethod, ErrorResponse, ErrorResponseType
from dotenv import load_dotenv

from utils import gen_password

load_dotenv()


class AccountViewSet(BaseViewSet):
    view_set_name = "account"
    queryset = Account.objects.select_related("profile").prefetch_related("roles")
    permission_classes = [MyActionPermission]
    serializer_class = AccountSerializer
    required_alternate_scopes = {
        "list": ["user:view_ger_info"],
        "retrieve": ["user:view_ger_info"],
        "reset_password": ["admin:reset_password"],
        "change_password": ["user:edit_public_info"],
    }

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(detail=False, methods=[HttpMethod.POST])
    def change_password(self, request, *args, **kwargs):
        account = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if check_password(old_password, account.password):
            account.password = make_password(new_password)
            account.save()
            return Response({"success": "Changed password!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error_message": "Old password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.PUT], detail=True)
    def reset_password(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            password = gen_password()
            instance.password = make_password(password)
            instance.save()
            AccountService.send_mail_reset_password(email=instance.email, password=password,
                                                    send_email=True)
            return Response({"success": "Reset password!"}, status=status.HTTP_200_OK)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.POST], detail=False)
    def reload_page(self, request, *args, **kwargs):
        account = request.user
        response_data = ProfileService.login_success_data(account.profile)
        if response_data:
            return Response(response_data)
