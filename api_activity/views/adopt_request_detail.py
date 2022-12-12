from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_activity.models import AdoptRequestDetail
from api_activity.serializers import RegisterAdoptRequestDetailSerializer, \
    AdoptRequestDetailSerializer
from api_activity.services import ProofService, AdoptRequestDetailService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType, HttpMethod


class AdoptRequestDetailViewSet(BaseViewSet):
    view_set_name = "adopt_request_detail"
    queryset = AdoptRequestDetail.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = AdoptRequestDetailSerializer
    required_alternate_scopes = {
        "create": ["adopt_request:create_adopt_request"]
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        data['adopter'] = request.user.profile.id
        serializer = RegisterAdoptRequestDetailSerializer(data=data)
        if serializer.is_valid(raise_exception=True) and AdoptRequestDetailService.check_request(data):
            with transaction.atomic():
                serializer.save()
                ProofService.update_proof_model(request, serializer.data.get("id"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["adopt_request_details"])
