from rest_framework.serializers import ModelSerializer

from api_activity.models import ActivityTypeGroup


class ActivityTypeGroupSerializer(ModelSerializer):
    class Meta:
        model = ActivityTypeGroup
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
