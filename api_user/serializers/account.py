from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_user.models import Account
from api_user.serializers import ProfileDetailSerializer


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"


class AccountGeneralInfo(ModelSerializer):
    profile = ProfileDetailSerializer()

    class Meta:
        model = Account
        fields = ['id', 'email', 'avatar', 'roles', 'profile']


class LoginAccountSerializer(ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    class Meta:
        model = Account
        fields = ["email", "password"]
