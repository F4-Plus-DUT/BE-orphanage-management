from rest_framework.serializers import ModelSerializer

from api_user.models import Role


class RoleSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"
        ordering = ('created_at', 'updated_at')
