from rest_framework.routers import DefaultRouter
from .views import PhysicalMedicalCaseViewSet

router = DefaultRouter()
router.register(
    r"cases",
    PhysicalMedicalCaseViewSet,
    basename="physical-medical-case"
)

urlpatterns = router.urls
