from rest_framework import routers

from .views import RoleViewSet, AccountViewSet, UserViewSet

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'role', RoleViewSet, basename='role')
router.register(r'account', AccountViewSet, basename='account')
router.register(r'', UserViewSet, basename='user')

urlpatterns = router.urls
