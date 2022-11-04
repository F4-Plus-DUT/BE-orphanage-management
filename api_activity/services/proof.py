import os

from api_activity.models import Proof, AdoptRequestDetail
from base.services import ImageService


class ProofService:
    @classmethod
    def update_proof_model(cls, request, adopt_request_detail_id):
        try:
            proof = request.FILES.getlist('proofs')
            request.data._mutable = True
            list_link = ImageService.upload_list_image(proof, os.getenv('CLOUDINARY_PROOF_FOLDER'))
            adopt_request_detail = AdoptRequestDetail.objects.filter(id = adopt_request_detail_id).first()
            list_proof = [Proof(link=link, adopt_request_detail=adopt_request_detail) for link in list_link]
            Proof.objects.bulk_create(list_proof)
            return True
        except Exception as e:
            print(e)
            return False
