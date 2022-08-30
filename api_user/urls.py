from rest_framework import routers

from .views import RoleViewSet

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'', RoleViewSet, basename='role')

urlpatterns = router.urls
