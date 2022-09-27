from rest_framework.serializers import ModelSerializer

from api_children.models import Children


class ChildrenSerializer(ModelSerializer):

    class Meta:
        model = Children
        fields = '__all__'
