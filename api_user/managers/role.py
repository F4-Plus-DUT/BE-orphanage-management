from django.db import models


class RoleManager(models.Manager):
    def by_name(self, name: str):
        return self.get_queryset().filter(name=name)

    def default(self):
        return self.get_queryset().filter(is_default=True).first()
