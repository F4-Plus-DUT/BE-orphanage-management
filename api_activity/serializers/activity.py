from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_activity.models import Activity, Comment


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        ordering = ('created_at', 'updated_at')


class ActivityDetailSerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        ordering = ('created_at', 'updated_at')

    def to_representation(self, instance):
        from api_statistic.models import Donor

        ret = super().to_representation(instance)
        total_donate = 0
        queryset = Donor.objects.by_activity(instance.id)
        for donate in queryset:
            total_donate += donate.ammount or 0
        ret["donate"] = total_donate
        return ret
