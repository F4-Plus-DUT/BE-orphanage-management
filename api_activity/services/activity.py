import os

from django.template.loader import render_to_string

from api_activity.models import Activity
from base.services import TokenUtil, ImageService
from base.services.send_mail import SendMail
from common.constants.image import ImageDefaultActivity


class ActivityService:
    @classmethod
    def init_data_children(cls, request):
        data = request.data.dict()
        personal_picture = request.FILES.get('cover_picture')
        if personal_picture:
            image_link = ImageService.upload_image(personal_picture, os.getenv('CLOUDINARY_ACTIVITY_FOLDER'))
            data['cover_picture'] = image_link
        else:
            data['cover_picture'] = ImageDefaultActivity.default_image
        return data

    # @classmethod
    # def send_notify(cls, serializer, base_link="{settings.UI_HOST}"):
    #     employee_role = Role.objects.by_id(RoleData.EMPLOYEE.value.get('id'))
    #     vip_donor = Profile.objects.vip_donor()
    #
    #     cls.send_mail(email=email, name=name, send_email=True, base_link=base_link)
    #     return {"success": True, "user": {"name": name, "email": email}}

    @classmethod
    def send_mail(
            cls,
            email=None,
            name=None,
            phone=None,
            personal_email=None,
            send_email=False,
            activity_type=None,
            content=None,
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
                [email, personal_email], "[F4plus Orphanage] New Activity", content
            )

    @classmethod
    def get_filter_query(cls, request):
        activity_type = request.query_params.get("activity_type")

        activity_type = activity_type if activity_type != 'all' else ''
        return Activity.objects.filter(activity_type__id=activity_type)
