from django.db import models


class ProfileManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(account__active=True)
