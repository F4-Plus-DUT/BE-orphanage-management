from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_children.models import Children


class ChildrenSerializer(ModelSerializer):
    name = serializers.CharField(required=False)
    gender = serializers.IntegerField(required=False)

    class Meta:
        model = Children
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
