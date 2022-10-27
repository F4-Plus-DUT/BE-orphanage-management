from api_activity.models import Comment


class CommentService:

    @classmethod
    def get_filter_query(cls, request):
        activity = request.query_params.get("activity")

        activity = activity if activity != 'all' else ''
        return Comment.objects.filter(activity__id=activity)

