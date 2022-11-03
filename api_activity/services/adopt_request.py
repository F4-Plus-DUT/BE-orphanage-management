from django.template.loader import render_to_string

from api_children.models import Children
from api_children.services import ChildrenService
from api_user.models import Profile
from api_user.statics import RoleData
from base.services import TokenUtil
from base.services.send_mail import SendMail
from common.constants.api_activity import AdoptRequestStatus
from common.constants.api_children import ChildrenStatus


class AdoptRequestService:
    @classmethod
    def send_notify(cls, serializer, base_link="{settings.UI_HOST}"):
        adopt_manager = Profile.objects.filter(account__roles__id_in=[RoleData.ADOPT_MANAGER.value.get('id'), RoleData.ADMIN.value.get('id')])
        adopter_name = Profile.objects.filter(id=serializer.data.get("adopter")).first().name
        children = Children.objects.filter(id=serializer.data.get("children")).first()
        children_name = children.name
        form_detail = serializer.data.get("form_detail")

        # update children_status
        ChildrenService.update_children_status(children, ChildrenStatus.PENDING)

        for manager in adopt_manager:
            personal_email = manager.personal_email if (not manager.account) or manager.personal_email != manager.account.email else None
            cls.send_mail(email=manager.account.email, name=manager.name, send_email=True, base_link=base_link,
                          personal_email=personal_email, adopter_name=adopter_name, children_name=children_name,
                          form_detail=form_detail)

    @classmethod
    def send_mail(
            cls,
            email=None,
            name=None,
            phone=None,
            personal_email=None,
            send_email=False,
            adopter_name="",
            children_name="",
            form_detail="",
            base_link="",
    ):
        if send_email:
            token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f"{base_link}?token={token}"
            content = render_to_string(
                "new_adopt_request.html",
                {"name": name, "adopter_name": adopter_name, "children_name": children_name, "form_detail": form_detail, "token": token},
            )
            SendMail.start(
                [email, personal_email], "[New Adopt Request] ", content
            )

    @classmethod
    def do_action(cls, adopt_request, approver, action):
        if action == AdoptRequestStatus.APPROVE:
            adopt_request = cls.update_request(adopt_request, approver, action)
            ChildrenService.update_children_status(adopt_request.children, ChildrenStatus.ADOPTED)
        elif action in [AdoptRequestStatus.REJECT, AdoptRequestStatus.CANCEL]:
            adopt_request = cls.update_request(adopt_request, approver, action)
            ChildrenService.update_children_status(adopt_request.children, ChildrenStatus.UNADOPTED)
        return adopt_request

    @classmethod
    def update_request(cls, adopt_request, approver, action):
        adopt_request.approver = approver
        adopt_request.action = action
        adopt_request.save()
        return adopt_request
