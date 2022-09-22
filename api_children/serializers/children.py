from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_children.models import Children


class ChildrenSerializer(ModelSerializer):
    adopter = serializers.SerializerMethodField()
    presenter = serializers.SerializerMethodField()

    class Meta:
        model = Children
        fields = '__all__'
