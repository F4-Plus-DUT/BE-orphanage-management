from django.template.loader import render_to_string

from api_activity.models import AdoptRequestDetail, AdoptRequest
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
        adopt_manager = Profile.objects.filter(account__roles__id__in=[RoleData.ADOPT_MANAGER.value.get('id'), RoleData.ADMIN.value.get('id')])
        adopter_name = AdoptRequestDetail.objects.filter(id=serializer.data.get("adopt_request_detail")).first().adopter.name
        children = Children.objects.filter(id=serializer.data.get("children")).first()
        children_name = children.name

        # update children_status
        ChildrenService.update_children_status(children, ChildrenStatus.PENDING)

        for manager in adopt_manager:
            personal_email = manager.personal_email if (not manager.account) or manager.personal_email != manager.account.email else None
            cls.send_mail(email=manager.account.email, name=manager.name, send_email=True, base_link=base_link,
                          personal_email=personal_email, adopter_name=adopter_name, children_name=children_name)

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
        adopter = adopt_request.adopt_request_detail.adopter
        personal_email = adopter.personal_email if (not adopter.account) or adopter.personal_email != adopter.account.email else None
        cls.action_send_mail(email=adopter.account.email,
                             name=adopter.name,
                             personal_email=personal_email,
                             send_email=True,
                             base_link="",
                             action=action,
                             approve_name=adopt_request.approver.name,
                             children_name=adopt_request.children.name
                             )
        return adopt_request

    @classmethod
    def action_send_mail(
            cls,
            email=None,
            name=None,
            phone=None,
            personal_email=None,
            send_email=False,
            action="",
            approve_name="",
            children_name="",
            base_link="",
    ):
        if send_email:
            # token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f"{base_link}?token="
            content = render_to_string(
                "action_adopt_request.html",
                {"name": name, "approve_name": approve_name, "action": action, "children_name": children_name, "token": ""},
            )
            SendMail.start(
                [email, personal_email], "[" + action + " Adopt Request]", content
            )

    @classmethod
    def update_request(cls, adopt_request, approver, action):
        adopt_request.approver = approver
        adopt_request.status = action
        adopt_request.save()
        return adopt_request

    @classmethod
    def check_action_request(cls, adopt_request, action):
        action_list = [AdoptRequestStatus.PENDING, AdoptRequestStatus.REJECT, AdoptRequestStatus.CANCEL,
                       AdoptRequestStatus.CANCELING, AdoptRequestStatus.APPROVE]
        if adopt_request.status in [AdoptRequestStatus.CANCEL, AdoptRequestStatus.REJECT]:
            return False
        elif adopt_request.status == AdoptRequestStatus.APPROVE:
            return False if action == AdoptRequestStatus.APPROVE or action == AdoptRequestStatus.REJECT else True
        return True if action_list in action_list else False

    @classmethod
    def get_filter_query(cls, request):
        status = request.query_params.get("status")
        inactive_status = [AdoptRequestStatus.REJECT, AdoptRequestStatus.CANCEL]
        query_set = AdoptRequest.objects.all()
        if status == AdoptRequestStatus.PENDING:
            return query_set.filter(status=AdoptRequestStatus.PENDING)
        if status == AdoptRequestStatus.APPROVE:
            return query_set.filter(status=AdoptRequestStatus.APPROVE)
        return query_set.filter(status__in=inactive_status)
