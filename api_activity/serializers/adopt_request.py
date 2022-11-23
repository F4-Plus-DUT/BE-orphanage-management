from rest_framework.serializers import ModelSerializer

from api_activity.models import AdoptRequest
from common.constants.api_activity import MapAdoptRequestStatus


class RegisterAdoptRequestSerializer(ModelSerializer):
    class Meta:
        model = AdoptRequest
        fields = ('children', 'adopt_request_detail')
        ordering = ('created_at', 'updated_at')


class AdoptRequestSerializer(ModelSerializer):
    from api_children.serializers import ChildrenSerializer

    children = ChildrenSerializer(read_only=True, required=False)

    class Meta:
        model = AdoptRequest
        fields = '__all__'
        ordering = ('created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for element in MapAdoptRequestStatus:
            if instance.status == element.value['value']:
                ret['status'] = element.value['id']
        ret["adopter_name"] = instance.adopt_request_detail.adopter.name
        ret["approver"] = instance.approver.name if instance.approver else None
        return ret
