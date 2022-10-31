from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_activity.models import Comment
from api_user.serializers.account import SortAccountSerializer


class CommentDetailSerializer(ModelSerializer):
    account = SortAccountSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', 'account', 'content', 'updated_at', 'content', 'parent')
        ordering = ('created_at', 'updated_at')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
