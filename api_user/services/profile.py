from typing import Optional

from django.db import transaction

from api_user.models import Profile
from api_user.serializers import ProfileDetailSerializer
from api_user.services import AccountService, RoleService, TokenService
from core.settings import SCOPES


class ProfileService:
    @classmethod
    @transaction.atomic
    def create_customer(cls, user_data: dict) -> Optional[Profile]:
        """
        Create a new user with new account and default role
        :param user_data:
        :return:
        """
        user = None
        account = user_data.pop('account', {})
        if account:
            default_role = RoleService.get_role_customer()
            account_instance = AccountService.create(account, default_role)
            user_data['account'] = account_instance
            user_data['personal_email'] = user_data.pop("email", None)
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
        - scopes
        - avatar
        - access_token
        - refresh_token
        - profile
        """
        token_data = TokenService.generate_by_account(profile.account)
        roles = profile.account.roles.all()
        scopes = ""
        for role in roles:
            scopes += (role.scope_text + " ")
        if scopes.__contains__("__all__"):
            scopes = " ".join(SCOPES.keys())
        user_data = {
            'email': profile.account.email,
            'avatar': profile.account.avatar,
            'permissions': scopes,
            'profile': ProfileDetailSerializer(profile).data
        }
        data = {**token_data, **user_data}
        return data
