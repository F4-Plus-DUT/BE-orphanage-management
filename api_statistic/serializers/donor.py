from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_statistic.models import Donor


class DonorSortSerializer(ModelSerializer):
    donor = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Donor
        fields = ('amount', 'created_at', 'donor')
        ordering = ('created_at', 'updated_at')

    @staticmethod
    def get_donor(self, obj):
        return obj.profile.name if obj.profile else "Ẩn Danh"


class DonorSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
