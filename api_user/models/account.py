from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from api_user.managers import AccountManager
from base.models import TimeStampedModel
from api_user.models import Role


class Account(AbstractBaseUser, TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name="users", null=True)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    class Meta:
        db_table = "accounts"
