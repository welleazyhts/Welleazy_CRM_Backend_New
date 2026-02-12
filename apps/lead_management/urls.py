from rest_framework.routers import DefaultRouter
from .views import LeadSourceViewSet, LeadStatusViewSet, LeadViewSet, IndividualClientViewSet

router = DefaultRouter()
router.register(r'sources', LeadSourceViewSet, basename='lead-source')
router.register(r'statuses', LeadStatusViewSet, basename='lead-status')
router.register(r'individual-clients', IndividualClientViewSet, basename='individual-client')
router.register(r'', LeadViewSet, basename='lead')

urlpatterns = router.urls
