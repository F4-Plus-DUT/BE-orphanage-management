from rest_framework import routers

from .views import RoleViewSet, AccountViewSet, ProfileViewSet

app_name = 'api_user'
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'role', RoleViewSet, basename='role')
router.register(r'account', AccountViewSet, basename='account')
router.register(r'', ProfileViewSet, basename='user')

urlpatterns = router.urls
