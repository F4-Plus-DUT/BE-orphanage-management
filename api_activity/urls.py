from rest_framework import routers

from api_activity.views.activity import ActivityViewSet

app_name = 'api_activity'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'', ActivityViewSet, basename='activity')


urlpatterns = router.urls
