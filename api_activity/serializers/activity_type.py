from rest_framework.serializers import ModelSerializer

from api_activity.models import ActivityType
from api_activity.serializers import ActivityTypeGroupSerializer


class ActivityTypeSerializer(ModelSerializer):
    activity_type_group = ActivityTypeGroupSerializer(read_only=True, required=False)

    class Meta:
        model = ActivityType
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
