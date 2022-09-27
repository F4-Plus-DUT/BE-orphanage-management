from django.db import models

from api_user.models import Account
from base.models import TimeStampedModel


class Donor(TimeStampedModel):
    donor_amount = models.FloatField(default=0)
    account = models.ForeignKey(Account, null=True, blank=True)
