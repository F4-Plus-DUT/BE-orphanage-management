from api_base.views import BaseViewSet
from api_user.models import Account
from api_user.serializers import AccountSerializer


class AccountViewSet(BaseViewSet):
    view_set_name = "account"
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
