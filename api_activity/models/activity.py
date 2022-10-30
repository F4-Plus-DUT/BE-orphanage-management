from django.utils import timezone
from django.db import models

from api_activity.models import ActivityType
from base.models import TimeStampedModel


class Activity(TimeStampedModel):
    title = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    cover_picture = models.CharField(max_length=255)
    expense = models.FloatField(default=0)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'activity'
