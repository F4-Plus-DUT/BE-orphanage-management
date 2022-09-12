from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models

from api_user.models import Account
from base.models import TimeStampedModel
from base.models.fields import TinyIntegerField


class Profile(TimeStampedModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    name = models.CharField(max_length=255)
    gender = TinyIntegerField(choices=GenderChoices.choices)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(
        max_length=11,
        null=True,
        validators=[
            RegexValidator(regex=r"^\d+$", message="A valid integer is required."),
            MinLengthValidator(9),
        ],
    )
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")

    class Meta:
        db_table = 'profiles'
