from django.db import models

from api_activity.models import AdoptRequestDetail
from api_children.models import Children
from api_user.models import Profile
from base.models import TimeStampedModel
from common.constants.api_activity import AdoptRequestStatus


class AdoptRequest(TimeStampedModel):
    children = models.ForeignKey(Children, on_delete=models.SET_NULL, null=True, blank=True)
    adopt_request_detail = models.ForeignKey(AdoptRequestDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name="adopt_request_detail")
    status = models.CharField(default=AdoptRequestStatus.PENDING, max_length=255, null=True, blank=True)
    approver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="approver")

    class Meta:
        db_table = 'adopt_request'
