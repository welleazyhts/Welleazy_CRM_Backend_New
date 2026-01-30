from rest_framework.routers import DefaultRouter
from .views import TestPackageViewSet

router = DefaultRouter()
router.register("test-packages", TestPackageViewSet, basename="test-packages")

urlpatterns = router.urls
