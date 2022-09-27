from datetime import timezone
from django.db import models

from api_activity.models import Activity
from api_user.models import Profile
from base.models import TimeStampedModel


class Donor(TimeStampedModel):
    donor_amount = models.FloatField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'donor'
