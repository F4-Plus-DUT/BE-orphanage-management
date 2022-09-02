from typing import Optional

from django.contrib.auth.hashers import make_password, check_password

from api_user.models import Account


class AccountService:
    @classmethod
    def create(cls, account_data) -> Account:
        """
        Create a new account.
        :param account_data:
        :return:
        """
        password = account_data.get('password', "")
        account_data['password'] = make_password(password)
        account = Account(**account_data)
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
        from api_user.services import UserService

        response_data = None
        email = login_data.get('email', "")
        password = login_data.get('password', "")
        account = Account.objects.by_email(email)
        if account and check_password(password, account.password):
            response_data = UserService.login_success_data(account.user)
        return response_data
