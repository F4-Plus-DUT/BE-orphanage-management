from django.db import transaction

from api_statistic.models import Donor


class DonorService:
    @classmethod
    def get_filter_query(cls, request):
        activity = request.query_params.get("activity")

        activity = None if activity == 'all' else activity

        filter_args = dict()

        if activity:
            filter_args.update(activity__id=activity)

        queryset = Donor.objects.filter(**filter_args)
        return queryset
