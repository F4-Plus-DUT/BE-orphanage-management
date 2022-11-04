from django.db import models

from api_activity.models import Activity
from api_statistic.managers import DonorManager
from api_user.models import Profile
from base.models import TimeStampedModel


class Donor(TimeStampedModel):
    amount = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=565, default="")
    objects = DonorManager()

    class Meta:
        db_table = 'donor'
