from api_user.models import Role
from api_user.statics import RoleData
from core.settings import SCOPES

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        admin_role = Role.objects.filter(id=RoleData.ADMIN.id).first()
        if admin_role:
            token['scopes'] = " ".join(SCOPES.keys())
        else:
            token['scopes'] = user.role.scope_text
        return token
