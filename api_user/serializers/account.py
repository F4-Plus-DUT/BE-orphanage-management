from rest_framework.serializers import ModelSerializer

from api_user.models import Account


class AccountSerializer(ModelSerializer):

    class Meta:
        models = Account
        fields = "__all__"
