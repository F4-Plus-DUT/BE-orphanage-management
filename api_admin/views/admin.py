import re

from api_admin.serializers.invite_list_serializer import InviteListSerializer
from api_admin.services import ExcelImportService, InviteListService
from base.serializers import InviteSerializer
from base.views import BaseViewSet
from api_user.services import AccountService
from common.constants.base import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminViewSet(BaseViewSet):
    http_method_names = [HttpMethod.POST]
    required_alternate_scopes = {
        "invite_list_user": ["admin:invite_user"],
        "invite": ["admin:invite_user"],
        "import_file": ["admin:invite_user"],
    }

    # TODO Update UI to use new endpoint
    @action(methods=[HttpMethod.POST], detail=False)
    def invite(self, request, *args, **kwargs):
        invite_serializer = InviteSerializer(data=request.data)
        invite_serializer.is_valid(raise_exception=True)

        email = request.data.get("email")
        name = request.data.get("name")
        base_link = request.build_absolute_uri("/verify")
        res = AccountService.invite(email, name, base_link)
        return Response(res)

    # TODO Move these 3 to separate view
    @action(methods=[HttpMethod.POST], detail=False, url_path="check-file")
    def check_file(self, request, *args, **kwargs):
        file = request.FILES["file"]
        try:
            if re.search(".xlsx$", file.name) and ".xlsx" in file.name:
                df = ExcelImportService().read_excel(file)
                df = df.rename(columns=str.lower)
                df_columns = set(df.columns.values)
                required_columns = {"name", "phone", "email"}

                if required_columns.issubset(df_columns):
                    df = df.drop(columns=list(df_columns.difference(required_columns)), axis=1)
                    if df.isnull().values.sum() > 0:
                        return Response(
                            {"message": "Contain null value"},
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                        )
                    rs = ExcelImportService().check_import(df=df)
                    return Response(rs)
            return Response(
                {"message": "File format error"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        except Exception as e:
            return Response(
                {"message": "File format error"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

    @action(methods=[HttpMethod.POST], detail=False, url_path="import-file")
    def import_file(self, request, *args, **kwargs):
        for row in request.data.get("rows"):
            if row.get("success"):
                base_link = request.build_absolute_uri("/verify")
                AccountService.send_mail(
                    email=row.get("email"),
                    name=row.get("name"),
                    phone=row.get("phone"),
                    send_email=True,
                    base_link=base_link,
                )
        return Response({"success": True})

    @action(methods=[HttpMethod.POST], detail=False, url_path="invite-users")
    def invite_list_user(self, request, *args, **kwargs):
        serializer = InviteListSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        invite_list_service = InviteListService()
        base_link = request.build_absolute_uri("/verify")
        valid_user, invalid_user = invite_list_service.separation_data(
            serializer.validated_data
        )
        for user in valid_user:
            AccountService.invite(
                email=user.get("email"), name=user.get("name"), base_link=base_link
            )
        data = {"valid_user": valid_user, "invalid_user": invalid_user}
        return Response(data=data, status=status.HTTP_201_CREATED)
