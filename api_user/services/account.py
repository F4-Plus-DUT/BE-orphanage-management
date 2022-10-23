import os

from typing import Optional

from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

from api_user.models import Account, Role, Profile
from api_user.statics import RoleData
from base.services import TokenUtil, ImageService
from base.services.send_mail import SendMail
from django.template.loader import render_to_string
from dotenv import load_dotenv

from utils import gen_password

load_dotenv()


class AccountService:
    @classmethod
    def create(cls, account_data, role: Role) -> Account:
        """
        Create a new account.
        :param account_data:
        -email
        -password
        :param role
        :return:
        """
        password = account_data.get('password', "")
        account_data['password'] = make_password(password)
        account = Account(**account_data)
        account.save()
        account.roles.add(role)
        account.save()
        return account

    @classmethod
    def login(cls, login_data) -> Optional[dict]:
        """
        Verify login data
        :param login_data:
        - email
        - password
        :return:
        general information if valid data
        else None
        """
        from api_user.services import ProfileService

        response_data = None
        email = login_data.get('email', "")
        password = login_data.get('password', "")
        account = Account.objects.by_email(email)
        if account and check_password(password, account.password):
            response_data = ProfileService.login_success_data(account.profile)
        return response_data

    @classmethod
    def invite(cls, email, name, base_link="{settings.UI_HOST}/verify"):
        password = gen_password()
        account_data = dict(
            email=email,
            password=password
        )
        employee_role = Role.objects.by_id(RoleData.EMPLOYEE.value.get('id'))
        cls.send_mail(email=email, name=name, password=password, send_email=True, base_link=base_link)
        with transaction.atomic():
            user = cls.create(account_data, employee_role)
            profile = Profile.objects.create(
                account=user,
                name=name,
                personal_email=email,
            )
        return {"success": True, "user": {"name": name, "email": email}}

    @classmethod
    def send_mail_reset_password(
            cls,
            email=None,
            phone=None,
            personal_email=None,
            send_email=False,
            base_link="",
            password="",
    ):
        if send_email:
            link = f"{base_link}"
            content = render_to_string(
                "reset_password.html",
                {"email": email, "password": password, "link": link},
            )
            SendMail.start(
                [email, personal_email], "[RESET PASSWORD] New generator password for your account", content
            )

    @classmethod
    def send_mail(
            cls,
            email=None,
            name=None,
            phone=None,
            personal_email=None,
            send_email=False,
            base_link="",
            password="",
    ):
        if send_email:
            token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f"{base_link}?token={token}"
            content = render_to_string(
                "invite_email.html",
                {"name": name, "email": email, "password": password, "link": link, "token": token},
            )
            SendMail.start(
                [email, personal_email], "Welcome to Orphanage Management", content
            )
