from rest_framework.serializers import ModelSerializer

from api_activity.models import AdoptRequest, AdoptRequestDetail
from api_activity.serializers import ProofSerializer
from api_user.serializers import AdopterSerializer


class RegisterAdoptRequestDetailSerializer(ModelSerializer):
    class Meta:
        model = AdoptRequestDetail
        fields = '__all__'
        ordering = ('created_at', 'updated_at')


class AdoptRequestDetailSerializer(ModelSerializer):
    adopter = AdopterSerializer(read_only=True, required=False)

    class Meta:
        model = AdoptRequestDetail
        fields = '__all__'
        ordering = ('created_at', 'updated_at')

    def to_representation(self, instance):
        from api_activity.models import Proof

        ret = super().to_representation(instance)
        queryset = Proof.objects.filter(adopt_request_detail__id=instance.id)
        ret["proof"] = ProofSerializer(queryset, many=True).data
        return ret
