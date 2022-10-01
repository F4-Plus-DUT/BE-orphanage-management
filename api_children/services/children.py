import os

from django.db.models import Value
from django.db.models.functions import Collate

from api_children.models import Children
from base.services import ImageService
from common.constants.base import Gender
from common.constants.image import ImageDefaultChildren


class ChildrenService:
    @classmethod
    def get_filter_query(cls, request):
        name = request.query_params.get("name")
        age = request.query_params.get("age")
        gender = request.query_params.get("gender")
        status = request.query_params.get("status")
        filter_args = dict()

        if age:
            filter_args.update(age=age)
        if gender:
            filter_args.update(gender=gender)
        if status:
            filter_args.update(status=status)
        if name:
            name = Collate(Value(name.strip()), "utf8mb4_general_ci")

        queryset = Children.objects.filter(name__icontains=name, **filter_args)
        return queryset

    @classmethod
    def init_data_children(cls, request):
        data = request.data.dict()
        gender = int(data.get('gender'))
        personal_picture = request.FILES.get('personal_picture')
        if personal_picture:
            image_link = ImageService.upload_image(personal_picture, os.getenv('CLOUDINARY_CHILDREN_FOLDER'))
            data['personal_picture'] = image_link
        else:
            data['personal_picture'] = ImageDefaultChildren.Female if gender == Gender.FEMALE else ImageDefaultChildren.Male
        return data
