from api_activity.models import ActivityType


class ActivityTypeService:
    @classmethod
    def get_filter_query(cls, request):
        group = request.query_params.get("group")

        group = group if group != 'all' else ''
        return ActivityType.objects.filter(activity_type_group__id=group)
