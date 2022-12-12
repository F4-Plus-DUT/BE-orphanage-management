from api_activity.models import AdoptRequestDetail


class AdoptRequestDetailService:
    @classmethod
    def check_request(cls, data):
        adopter = data.get("adopter")
        count = AdoptRequestDetail.objects.filter(adopter=adopter).count()
        if count > 5:
            return False
        return True
