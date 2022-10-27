from django.db import models


class CommentManager(models.Manager):
    def by_activity(self, activity_id):
        return self.get_queryset().filter(activity__id=activity_id)
