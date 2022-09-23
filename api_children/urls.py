from rest_framework import routers

from api_children.views import ChildrenViewSet

app_name = 'api_children'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'', ChildrenViewSet, basename='children')

urlpatterns = router.urls
