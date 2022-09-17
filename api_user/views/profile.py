from api_user.models.profile import Profile
from api_user.serializers import ProfileSerializer
from base.views import BaseViewSet


class ProfileViewSet(BaseViewSet):
    view_set_name = "profile"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
