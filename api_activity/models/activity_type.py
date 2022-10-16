from django.db import models

from api_activity.models import ActivityTypeGroup
from base.models import TimeStampedModel


class ActivityType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    activity_type_group = models.ForeignKey(ActivityTypeGroup, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'activity_type'
