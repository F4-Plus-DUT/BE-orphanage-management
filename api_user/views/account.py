from api_user.models import Account
from api_user.serializers import AccountSerializer
from api_user.serializers.account import AccountGeneralInfo
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    view_set_name = "account"
    queryset = Account.objects.select_related("profile").prefetch_related("roles")
    permission_classes = [MyActionPermission]
    serializer_class = AccountSerializer
    serializer_map = {
        "retrieve": AccountGeneralInfo,
        "list": AccountGeneralInfo,
    }
    required_alternate_scopes = {
        "list": ["user:view_ger_info"],
        "retrieve": ["user:view_ger_info"]
    }

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)
