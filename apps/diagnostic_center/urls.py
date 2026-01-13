from rest_framework.routers import DefaultRouter
from .views import DiagnosticCenterViewSet

router = DefaultRouter()
router.register("diagnostic-centers", DiagnosticCenterViewSet, basename="diagnostic-center")

urlpatterns = router.urls
