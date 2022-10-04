from rest_framework import routers

from .views import AdminViewSet

app_name = "api_admin"
router = routers.SimpleRouter(trailing_slash=True)

router.register(r"", AdminViewSet, basename="admins")

urlpatterns = router.urls
