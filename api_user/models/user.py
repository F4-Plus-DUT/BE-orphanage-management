from django.db import models

from api_user.models import Account
from base.models import TimeStampedModel
from base.models.fields import TinyIntegerField


class User(TimeStampedModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = TinyIntegerField(choices=GenderChoices.choices)
    birthday = models.DateField(null=True, blank=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'
