import os
from typing import Optional

from django.db import transaction
from django.db.models import Value, Q
from django.db.models.functions import Collate

from api_statistic.models import Donor
from api_user.models import Profile
from api_user.serializers import ProfileDetailSerializer
from api_user.services import AccountService, TokenService
from base.services import ImageService
from core.settings import SCOPES


class ProfileService:
    @classmethod
    @transaction.atomic
    def create_profile(cls, role, user_data: dict) -> Optional[Profile]:
        """
        Create a new user with new account by role
        :param user_data:
        :param role:
        :return:
        """
        user = None
        account = user_data.pop('account', {})
        if account:
            password = account.get('password', "")
            account_instance = AccountService.create(account, role)
            user_data['account'] = account_instance
            user_data['personal_email'] = account_instance.email
            user_data['is_vip_donor'] = user_data.pop("is_vip_donor", False)
            user = Profile(**user_data)
            user.save()
            AccountService.send_mail(email=account.get('email', ""), name=user.name, personal_email=user.personal_email,
                                     send_email=True, password=password)
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

    @classmethod
    def get_filter_query(cls, request, queryset):
        name = request.query_params.get("name")
        if name:
            name = Collate(Value(name.strip()), "utf8mb4_general_ci")

        queryset = queryset.filter(Q(name__icontains=name) | Q(personal_email__icontains=name))
        return queryset

    @classmethod
    def init_data_profile(cls, request, instance):
        data = request.data.dict()
        account = instance.account
        if account:
            avatar = request.FILES.get('avatar')
            if avatar:
                image_link = ImageService.upload_image(avatar, os.getenv('CLOUDINARY_AVATAR_FOLDER'))
                account.avatar = image_link
                account.save()
        return data

    @classmethod
    def update_vip_donor(cls, profile_id):
        profile = Profile.objects.filter(id=profile_id).first()
        count_donor = Donor.objects.filter(profile=profile).count()
        profile.is_vip_donor = True if count_donor >= 3 else profile.is_vip_donor
        profile.save()
        return profile
