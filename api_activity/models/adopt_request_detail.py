from django.db import models

from api_user.models import Profile
from base.models import TimeStampedModel
from base.models.fields import TinyIntegerField


class AdoptRequestDetail(TimeStampedModel):
    class MaritalStatusChoices(models.IntegerChoices):
        SINGLE = 1
        MARRIED = 2
        OTHER = 3
    adopter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="adopter")
    income = models.CharField(max_length=235, null=True, blank=True)
    marital_status = TinyIntegerField(choices=MaritalStatusChoices.choices, default=MaritalStatusChoices.SINGLE)
    family_status = models.BooleanField(default=0)

    class Meta:
        db_table = 'adopt_request_details'
