from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_user.models import Account
from api_user.serializers import LoginAccountSerializer, AccountSerializer
from api_user.serializers.profile import ProfileSerializer
from api_user.services import AccountService, TokenService, ProfileService
from common.constants.base import HttpMethod, ErrorResponse, ErrorResponseType
from base.views import BaseViewSet


class ActionViewSet(BaseViewSet):
    permission_classes = []
    view_set_name = "action"
    queryset = Account.objects.all().prefetch_related("roles")
    serializer_class = AccountSerializer
    serializer_map = {
        "login": LoginAccountSerializer,
        "sign_up": ProfileSerializer,
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
            user = ProfileService.create_customer(serializer.validated_data)
            if user:
                resp = ProfileService.login_success_data(user)
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
