from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_statistic.models import Donor
from api_statistic.serializers import DonorSerializer
from api_statistic.services import DonorService
from api_user.services import ProfileService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType


class DonorViewSet(BaseViewSet):
    view_set_name = "donor"
    queryset = Donor.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = DonorSerializer
    required_alternate_scopes = {
        "retrieve": ["statistic:view_statistic"],
        "list": [],
        "update": ["None"],
        "create": [],
        "destroy": ["None"],
    }

    def list(self, request, *args, **kwargs):
        queryset = DonorService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['profile'] = None if request.user.is_anonymouse else request.user.profile.id
        data['activity'] = None if data['activity'] == "" or data['activity'] == "undefined" else data['activity']

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                if not request.user.is_anonymouse:
                    ProfileService.update_vip_donor(request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["donor"])
