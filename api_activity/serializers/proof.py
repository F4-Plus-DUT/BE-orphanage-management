from rest_framework.serializers import ModelSerializer

from api_activity.models import Proof


class ProofSerializer(ModelSerializer):
    class Meta:
        model = Proof
        fields = ('id', 'link')
        ordering = ('created_at', 'updated_at')
