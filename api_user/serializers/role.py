from rest_framework.serializers import ModelSerializer

from api_user.models import Role


class RoleSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ['name']
