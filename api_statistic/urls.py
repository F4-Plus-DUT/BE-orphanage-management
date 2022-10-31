from rest_framework import routers

from api_statistic.views import DonorViewSet

app_name = 'api_statistic'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'donate', DonorViewSet, basename='donor')

urlpatterns = router.urls
