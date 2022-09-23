from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_children.models import Children
from api_user.serializers import LiveCustomerProfile


class ChildrenSerializer(ModelSerializer):
    adopter = LiveCustomerProfile(required=False)
    presenter = LiveCustomerProfile(required=False)

    class Meta:
        model = Children
        fields = '__all__'
