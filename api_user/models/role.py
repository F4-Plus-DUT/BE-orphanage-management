from django.db import models

from api_user.managers import RoleManager
from base.models import TimeStampedModel


class Role(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    scope_text = models.TextField(default="", blank=True)
    description = models.TextField()
    last_modified_by = models.CharField(max_length=255, default="", blank=True)
    levels = models.IntegerField(default=4, null=True, blank=True)

    objects = RoleManager()

    class Meta:
        db_table = 'roles'
        ordering = ('created_at',)
