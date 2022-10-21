from django.db import models

from api_children.models import Children
from api_user.models import Profile
from base.models import TimeStampedModel
from common.constants.api_activity import AdoptRequestStatus


class AdoptRequest(TimeStampedModel):
    children = models.ForeignKey(Children, on_delete=models.SET_NULL, null=True, blank=True)
    adopter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="adopter")
    form_detail = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(default="Pending", max_length=255, null=True, blank=True)
    approver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="approver")

    class Meta:
        db_table = 'adopt_request'
