from django.db import models


class AccountManager(models.Manager):
    def by_email(self, email: str):
        email = email.strip()
        return self.get_queryset().filter(email=email).first()

    def by_id(self, pk):
        return self.get_queryset().filter(id=pk).first()
