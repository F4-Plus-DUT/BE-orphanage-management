from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_statistic.models import Donor


class DonorSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
