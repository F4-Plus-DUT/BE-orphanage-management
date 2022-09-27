from django.utils import timezone
from django.db import models
from base.models import TimeStampedModel


class Activity(TimeStampedModel):
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    picture = models.CharField(max_length=255)
    expense = models.FloatField(default=0)
    activity_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'activity'
