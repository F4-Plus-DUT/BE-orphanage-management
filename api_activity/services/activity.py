import os

from django.template.loader import render_to_string

from api_activity.models import Activity, ActivityType
from api_user.models import Role, Profile
from api_user.statics import RoleData
from base.services import TokenUtil, ImageService
from base.services.send_mail import SendMail
from common.constants.image import ImageDefaultActivity
from itertools import chain


class ActivityService:
    @classmethod
    def init_data_activity(cls, request):
        data = request.data.dict()
        personal_picture = request.FILES.get('cover_picture')
        if personal_picture:
            image_link = ImageService.upload_image(personal_picture, os.getenv('CLOUDINARY_ACTIVITY_FOLDER'))
            data['cover_picture'] = image_link
        else:
            data['cover_picture'] = ImageDefaultActivity.default_image
        return data

    @classmethod
    def upload_image_data_activity(cls, request):
        data = request.data.dict()
        personal_picture = request.FILES.get('cover_picture')
        if personal_picture:
            image_link = ImageService.upload_image(personal_picture, os.getenv('CLOUDINARY_ACTIVITY_FOLDER'))
            data['cover_picture'] = image_link
        return data

    @classmethod
    def send_notify(cls, serializer, base_link="{settings.UI_HOST}"):
        vip_donor = Profile.objects.vip_donor()
        employee = Profile.objects.filter(account__roles__id=RoleData.EMPLOYEE.value.get('id'))
        all_profile_to_send_mail = list(chain(vip_donor, employee))
        valid_user, invalid_user = cls.separation_profile(all_profile_to_send_mail)

        activity_type = ActivityType.objects.filter(id=serializer.get("activity_type")).first().name
        content = serializer.get("content")
        title = serializer.get("title")

        for user in valid_user:
            personal_email = user.personal_email if (not user.account) or user.personal_email != user.account.email else None
            cls.send_mail(email=user.account.email, name=user.name, send_email=True, base_link=base_link,
                          personal_email=personal_email, activity_type=activity_type, content=content, title=title)

    @classmethod
    def separation_profile(cls, profiles: list):
        valid_profile = []
        valid_email = []
        invalid_profile = []

        for profile in profiles:
            if profile.account:
                if profile.account.email in valid_email or profile.personal_email in valid_email:
                    invalid_profile.append(profile)
                    continue
                valid_profile.append(profile)
                valid_email.append(profile.account.email)
                if profile.personal_email != profile.account.email:
                    valid_email.append(profile.personal_email)
            else:
                if profile.personal_email in valid_email:
                    invalid_profile.append(profile)
                    continue
                valid_profile.append(profile)
                valid_email.append(profile.personal_email)
        return valid_profile, invalid_profile

    @classmethod
    def send_mail(
            cls,
            email=None,
            name=None,
            phone=None,
            personal_email=None,
            send_email=False,
            activity_type="",
            content=None,
            title="",
            base_link="",
    ):
        if send_email:
            token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f"{base_link}?token={token}"
            content = render_to_string(
                "new_activity.html",
                {"name": name, "activity_type": activity_type, "content": content, "link": link, "token": token},
            )
            SendMail.start(
                [email, personal_email], "[New Activity] " + title, content
            )

    @classmethod
    def get_filter_query(cls, request):
        activity_type = request.query_params.get("activity_type")
        query_set = Activity.objects.all()
        if activity_type == 'all':
            return query_set
        return Activity.objects.filter(activity_type__id=activity_type)
