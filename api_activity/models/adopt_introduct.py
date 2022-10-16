from django.db import models

from api_activity.models import ActivityType
from api_children.models import Children
from api_user.models import Profile
from base.models import TimeStampedModel


class AdoptIntroductActivity(TimeStampedModel):
    children = models.ForeignKey(Children, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'adopt_introduction'
