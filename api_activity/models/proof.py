from django.db import models

from api_activity.models import AdoptRequestDetail
from base.models import TimeStampedModel


class Proof(TimeStampedModel):
    link = models.CharField(max_length=255, default="", blank=True)
    adopt_request_detail = models.ForeignKey(AdoptRequestDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name="proof")

    class Meta:
        db_table = 'proofs'
        ordering = ('created_at',)
