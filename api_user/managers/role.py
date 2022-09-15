import uuid

from django.db import models

from api_user.statics import RoleData


class RoleManager(models.Manager):
    def by_name(self, name: str):
        return self.get_queryset().filter(name=name)

    def by_id(self, role_id: uuid):
        return self.get_queryset().filter(id=role_id).first()

    def default(self):
        return self.get_queryset().filter(id=RoleData.CUSTOMER.value.get('id')).first()
