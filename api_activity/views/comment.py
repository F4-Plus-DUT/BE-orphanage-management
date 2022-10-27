from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_activity.models import Comment
from api_activity.serializers import CommentSerializer
from api_activity.services import CommentService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType


class CommentViewSet(BaseViewSet):
    view_set_name = "comment"
    queryset = Comment.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = CommentSerializer
    pagination_class = None
    required_alternate_scopes = {
        "list": [],
        "create": ['activity:comment_activity'],
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        data['parent'] = None if data['parent'] == "" or data['parent'] == "undefined" else data['parent']
        data['account'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["comment"])

    def list(self, request, *args, **kwargs):
        queryset = CommentService.get_filter_query(request)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
