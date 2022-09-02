from api_user.models.user import User
from api_user.serializers import UserSerializer
from base.views import BaseViewSet


class UserViewSet(BaseViewSet):
    view_set_name = "user"
    queryset = User.objects.all()
    serializer_class = UserSerializer
