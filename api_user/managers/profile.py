from django.db import models


class ProfileManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(account__active=True)

    def vip_donor(self):
        return self.get_queryset().filter(is_vip_donor=True)
