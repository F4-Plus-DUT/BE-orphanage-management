import datetime

from django.db import models

from api_user.models import Profile
from base.models import TimeStampedModel
from base.models.fields import TinyIntegerField
from common.constants.api_children import ChildrenStatus


class Children(TimeStampedModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    name = models.CharField(max_length=255)
    gender = TinyIntegerField(choices=GenderChoices.choices)
    age = models.IntegerField(null=True, blank=True)
    personal_picture = models.CharField(max_length=255, null=True, blank=True)
    join_date = models.DateField(default=datetime.datetime.now(), null=True, blank=True)
    adopt_date = models.DateField(null=True, blank=True)
    status = models.CharField(default=ChildrenStatus.UNADOPTED, max_length=10)
    adopter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='adopter')
    presenter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='presenter')

    class Meta:
        db_table = 'children'