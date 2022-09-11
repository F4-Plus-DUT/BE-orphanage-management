from rest_framework import routers

app_name = 'base'
router = routers.SimpleRouter(trailing_slash=True)


urlpatterns = router.urls
