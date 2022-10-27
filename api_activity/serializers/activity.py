from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_activity.models import Activity, Comment


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        ordering = ('created_at', 'updated_at')


class ActivityDetailSerializer(ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'
        ordering = ('created_at', 'updated_at')

    def get_comments(self, obj):
        from api_activity.serializers import CommentDetailSerializer
        from api_activity.models import Comment

        queryset = Comment.objects.by_activity(obj.id)
        return CommentDetailSerializer(queryset, many=True).data