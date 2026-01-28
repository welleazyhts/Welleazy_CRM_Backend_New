from rest_framework.routers import DefaultRouter
from .views import IndividualTestViewSet

router = DefaultRouter()
router.register(r"individual-tests",IndividualTestViewSet,basename="individual-tests")

urlpatterns = router.urls
