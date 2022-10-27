from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_user.models import Account


class AccountSerializer(ModelSerializer):
    email = serializers.EmailField(read_only=True, required=False)

    class Meta:
        model = Account
        exclude = ['password']
        ordering = ('created_at', 'updated_at')


class SortAccountSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'name', 'avatar', 'email')
        ordering = ('created_at', 'updated_at')

    def get_name(self, obj):
        return obj.profile.name or 'No Name'


class LoginAccountSerializer(ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    class Meta:
        model = Account
        fields = ["email", "password"]
