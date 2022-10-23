from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_user.models import Account


class AccountSerializer(ModelSerializer):
    email = serializers.EmailField(read_only=True, required=False)

    class Meta:
        model = Account
        exclude = ['password']
        ordering = ('created_at', 'updated_at')


class LoginAccountSerializer(ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    class Meta:
        model = Account
        fields = ["email", "password"]
