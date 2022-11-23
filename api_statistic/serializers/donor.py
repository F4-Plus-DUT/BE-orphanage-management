from rest_framework.serializers import ModelSerializer

from api_statistic.models import Donor


class DonorSortSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = ('id', 'amount', 'created_at', 'note')
        ordering = ('created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["donor"] = instance.profile.name if instance.profile else "Ẩn Danh"
        ret["activity"] = instance.activity.title if instance.activity else "Ủng hộ trung tâm"
        return ret


class DonorSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'
        ordering = ('created_at', 'updated_at')
