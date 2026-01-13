from rest_framework.routers import DefaultRouter
from apps.cases.views import CaseViewSet

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='cases')

urlpatterns = router.urls
