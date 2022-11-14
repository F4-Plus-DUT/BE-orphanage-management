from datetime import datetime, timedelta
import time
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_statistic.models import Donor
from api_statistic.serializers import DonorSerializer, DonorSortSerializer
from api_statistic.services import DonorService
from api_user.services import ProfileService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType, HttpMethod


class DonorViewSet(BaseViewSet):
    view_set_name = "donor"
    queryset = Donor.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = DonorSerializer
    serializer_map = {
        "list": DonorSortSerializer
    }
    required_alternate_scopes = {
        "retrieve": ["statistic:view_statistic"],
        "list": [],
        "update": ["None"],
        "create": [],
        "destroy": ["None"],
        "get_donate_statistics": ["statistic:view_statistic"],
    }

    def list(self, request, *args, **kwargs):
        queryset = DonorService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.pop("email", None)
        data['profile'] = None if request.user.is_anonymous else request.user.profile.id
        data['activity'] = None if data['activity'] == "" or data['activity'] == "undefined" else data['activity']

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                DonorService.send_mail_to_donor(serializer, email)
            if not request.user.is_anonymous:
                ProfileService.update_vip_donor(request.user.profile.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["donor"])

    @action(methods=[HttpMethod.GET], detail=False)
    def get_donate_statistics(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date", "")
        end_date = request.query_params.get("end_date", "")

        if not start_date or not end_date:
            return Response({"detail": "Not found start_date and end_date in url param"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            check_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            check_end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if check_start_date > check_end_date:
                raise ValueError
        except ValueError:
            return Response({"detail": "Invalid start_date/end_date"}, status=status.HTTP_400_BAD_REQUEST)

        donate_statistics = DonorService.get_donate_statistics(start_date, end_date)
        return Response(donate_statistics)
