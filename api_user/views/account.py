from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_user.models import Account
from api_user.serializers import AccountSerializer, LoginAccountSerializer
from api_user.serializers.user import CUUserSerializer
from api_user.services import AccountService, UserService, TokenService
from base.consts import HttpMethod, ErrorResponse, ErrorResponseType
from base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    view_set_name = "account"
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    serializer_map = {
        "sign_in": LoginAccountSerializer,
        "sign_up": CUUserSerializer,
    }

    @action(detail=False, methods=[HttpMethod.POST])
    def sign_in(self, request, *args, **kwargs):
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
            user = UserService.create(serializer.validated_data)
            if user:
                resp = UserService.login_success_data(user)
                return Response(resp, status=status.HTTP_201_CREATED)
            else:
                return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["user"])

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
