from django.db import models

from api_user.managers import RoleManager
from base.models import TimeStampedModel


class Role(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    scope_text = models.TextField()
    description = models.TextField()
    is_default = models.BooleanField(default=False)

    objects = RoleManager()

    class Meta:
        db_table = 'roles'
        ordering = ('created_at',)
