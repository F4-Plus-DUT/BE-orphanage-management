
import json

import factory
from api_user.models import Profile, Account
from faker import Factory
from rest_framework.test import APIClient

faker = Factory.create()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile


def authentication(user):
    client = APIClient()
    url = "/api/v1/login/"
    payload = {"email": user.email, "password": "defaultpassword"}
    res = client.post(url, data=payload)
    response_data = json.loads(res.content)
    token = response_data.get("token")
    return token
