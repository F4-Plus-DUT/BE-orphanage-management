from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from api_user.models import Account
from api_user.models.profile import Profile


class ProfileDetailSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['account', 'is_active']


class ProfileSerializer(ModelSerializer):
    email = serializers.EmailField(source='account.email')
    password = serializers.CharField(min_length=8, source="account.password")
    avatar = serializers.CharField(source='account.avatar', required=False)

    def validate_email(self, value):
        duplicated_email = Account.objects.by_email(value)
        if duplicated_email is not None:
            raise ValidationError("Email already exists.")
        return value

    class Meta:
        model = Profile
        fields = ('id', 'name', 'gender', 'email', 'password', 'avatar')
