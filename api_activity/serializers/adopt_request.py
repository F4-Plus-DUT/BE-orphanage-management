from rest_framework.serializers import ModelSerializer

from api_activity.models import AdoptRequest


class RegisterAdoptRequestSerializer(ModelSerializer):
    class Meta:
        model = AdoptRequest
        fields = ('children', 'adopt_request_detail')
        ordering = ('created_at', 'updated_at')


class AdoptRequestSerializer(ModelSerializer):
    from api_activity.serializers import RegisterAdoptRequestDetailSerializer
    from api_children.serializers import ChildrenSerializer

    adopt_request_detail = RegisterAdoptRequestDetailSerializer(read_only=True, required=False)
    children = ChildrenSerializer(read_only=True, required=False)

    class Meta:
        model = AdoptRequest
        fields = '__all__'
        ordering = ('created_at', 'updated_at')