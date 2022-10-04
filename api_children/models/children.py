
from django.db import models

from django.utils import timezone
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
    join_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    status = models.CharField(default=ChildrenStatus.UNADOPTED, max_length=10)
    identifier = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        db_table = 'children'
