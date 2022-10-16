from django.db import models
from base.models import TimeStampedModel


class ActivityTypeGroup(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'activity_type_group'
