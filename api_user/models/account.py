from django.db import models

from api_base.models import TimeStampedModel
from api_user.models import Role


class Account(TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "accounts"
