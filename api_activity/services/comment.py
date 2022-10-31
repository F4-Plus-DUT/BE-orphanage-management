from api_activity.models import Comment


class CommentService:

    @classmethod
    def get_filter_query(cls, request):
        activity = request.query_params.get("activity")

        activity = '' if activity == 'all' or activity == 'undefined' else activity
        return Comment.objects.filter(activity=activity)
