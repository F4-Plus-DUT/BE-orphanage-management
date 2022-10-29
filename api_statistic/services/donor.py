from django.db import transaction

from api_statistic.models import Donor


class DonorService:
    @classmethod
    def get_filter_query(cls, request):
        activity = request.query_params.get("activity")
        donor = request.query_params.get("donor")

        activity = None if activity == 'all' else activity
        donor = None if donor == 'all' else donor

        filter_args = dict()

        if activity:
            filter_args.update(activity__id=activity)
        if donor:
            filter_args.update(profile__id=donor)

        queryset = Donor.objects.filter(**filter_args)
        return queryset