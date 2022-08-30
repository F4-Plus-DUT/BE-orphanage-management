from django.db import models
from django.db.models import Manager
from django.utils import timezone


class BaseSimpleModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = Manager

    class Meta:
        abstract = True
