from rest_framework import routers

from api_activity.views import ActivityViewSet, ActivityTypeGroupViewSet, ActivityTypeViewSet, AdoptRequestViewSet, \
    CommentViewSet, AdoptRequestDetailViewSet

app_name = 'api_activity'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'activity_type_group', ActivityTypeGroupViewSet, basename='activity_type_group')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'adopt_request_detail', AdoptRequestDetailViewSet, basename='adopt_request')
router.register(r'adopt_request', AdoptRequestViewSet, basename='adopt_request')
router.register(r'activity_type', ActivityTypeViewSet, basename='activity_type')
router.register(r'', ActivityViewSet, basename='activity')

urlpatterns = router.urls
