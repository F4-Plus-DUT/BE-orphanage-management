from typing import Optional

from django.db import transaction

from api_user.models.profile import Profile
from api_user.services import AccountService, RoleService, TokenService


class UserService:
    @classmethod
    @transaction.atomic
    def create(cls, user_data: dict) -> Optional[Profile]:
        """
        Create a new user with new account and default role
        :param user_data:
        :return:
        """
        user = None
        account = user_data.pop('account', {})
        if account:
            default_role = RoleService.get_default_role()
            account['role'] = default_role
            account_instance = AccountService.create(account)
            user_data['account'] = account_instance
            user = Profile(**user_data)
            user.save()
        return user

    @classmethod
    def login_success_data(cls, user: Profile):
        """
        Return success data for login
        :param user:
        :return: dictionary data with general user information and token
        included fields:
        - id
        - first_name
        - last_name
        - avatar
        - access_token
        - refresh_token
        """
        token_data = TokenService.generate_by_account(user.account)
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.account.avatar,
        }
        data = {**token_data, **user_data}
        return data
