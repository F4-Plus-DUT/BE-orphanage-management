from rest_framework.serializers import ModelSerializer

from api_activity.models import AdoptRequest


class RegisterAdoptRequestSerializer(ModelSerializer):
    class Meta:
        model = AdoptRequest
        fields = ('children', 'form_detail', 'adopter')
        ordering = ('created_at', 'updated_at')


class AdoptRequestSerializer(ModelSerializer):
    class Meta:
        model = AdoptRequest
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
