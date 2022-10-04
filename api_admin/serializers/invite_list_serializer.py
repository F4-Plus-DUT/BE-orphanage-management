from api_user.models import Account
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class InviteListSerializer(serializers.Serializer):
    def validate(self, attrs):
        email = attrs.get("email")
        name = attrs.get("name")
        validator = EmailValidator()
        try:
            # Todo: if you would like to whitelist the email, toggle these lines
            # validator(allowlist=['paradox.ai'])
            validator(email)
        except ValidationError:
            return {
                "email": email,
                "name": name,
                "status": "Invalid email format",
                "success": False,
            }

        existed = Account.objects.filter(email=email).count()
        if existed:
            return {
                "email": email,
                "name": name,
                "status": "Already existed",
                "success": False,
            }
        return {"email": email, "name": name, "status": "Success", "success": True}

    name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
