from typing import Optional

from django.db import transaction

from api_user.models.profile import Profile
from api_user.services import AccountService, RoleService, TokenService
from core.settings import SCOPES


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
    def login_success_data(cls, profile: Profile):
        """
        Return success data for login
        :param profile:
        :return: dictionary data with general user information and token
        included fields:
        - id
        - name
        - scopes
        - avatar
        - access_token
        - refresh_token
        """
        token_data = TokenService.generate_by_account(profile.account)
        roles = profile.account.roles.all()
        scopes = ""
        for role in roles:
            scopes += (role.scope_text + " ")
        if scopes.__contains__("__all__"):
            scopes = " ".join(SCOPES.keys())
        user_data = {
            'id': profile.id,
            'name': profile.name,
            'avatar': profile.account.avatar,
            'scopes': scopes
        }
        data = {**token_data, **user_data}
        return data
