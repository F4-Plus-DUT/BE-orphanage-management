from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_user.models import Account, Profile
from api_user.serializers import LoginAccountSerializer, AccountSerializer
from api_user.serializers.profile import ProfileSerializer
from api_user.services import AccountService, TokenService, ProfileService, RoleService
from common.constants.base import HttpMethod, ErrorResponse, ErrorResponseType
from base.views import BaseViewSet
from account_utils import gen_password


class ActionViewSet(BaseViewSet):
    permission_classes = []
    view_set_name = "action"
    queryset = Account.objects.all().prefetch_related("roles")
    serializer_class = AccountSerializer
    serializer_map = {
        "login": LoginAccountSerializer,
        "sign_up": ProfileSerializer,
        "register_email": ProfileSerializer,
    }

    @action(detail=False, methods=[HttpMethod.POST])
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            login_data = AccountService.login(serializer.validated_data)
            if login_data:
                return Response(login_data)
            else:
                return ErrorResponse(ErrorResponseType.GENERAL, params=["email/password invalid"])

    @action(detail=False, methods=[HttpMethod.POST])
    def sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = ProfileService.create_profile(RoleService.get_role_customer(), serializer.validated_data)
            if user:
                resp = ProfileService.login_success_data(user)
                return Response(resp, status=status.HTTP_201_CREATED)
            else:
                return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["user"])

    @action(methods=[HttpMethod.POST], detail=False)
    def register_email(self, request, *args, **kwargs):
        account = request.user
        if account.is_anonymous:
            data = request.data
            data["is_vip_donor"] = True
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                profile = ProfileService.create_profile(RoleService.get_role_customer(), serializer.validated_data)
        else:
            profile = Profile.objects.filter(account=account).first()
            profile.is_vip_donor = True
            profile.save()
        return Response({"message": "Success register mail"}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.POST], detail=False)
    def forgot_password(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            account = Account.objects.by_email(email)
            if account:
                password = gen_password()
                account.password = make_password(password)
                account.save()
                AccountService.send_mail_reset_password(email=account.email,
                                                        password=password, send_email=True)
                return Response({"success": "Reset password!"}, status=status.HTTP_200_OK)
        return Response({"error_message": "Email is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=[HttpMethod.GET])
    def refresh_new_token(self, request, *args, **kwargs):
        token = request.query_params.get("token", "")
        response_data = {}

        if token:
            response_data = TokenService.refresh_new_token(token)

        if response_data:
            return Response(response_data)
        else:
            return ErrorResponse(ErrorResponseType.INVALID, params=["token"])
