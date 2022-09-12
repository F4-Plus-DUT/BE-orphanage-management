from rest_framework.permissions import IsAuthenticated

from api_user.models import Account
from api_user.serializers import AccountSerializer
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    view_set_name = "account"
    queryset = Account.objects.all().prefetch_related("roles")
    permission_classes = [MyActionPermission | IsAuthenticated]
    serializer_class = AccountSerializer
    serializer_map = {}
