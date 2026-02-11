from rest_framework.routers import DefaultRouter
from .views import LeadSourceViewSet, LeadStatusViewSet, LeadViewSet

router = DefaultRouter()
router.register(r'sources', LeadSourceViewSet, basename='lead-source')
router.register(r'statuses', LeadStatusViewSet, basename='lead-status')
router.register(r'', LeadViewSet, basename='lead')

urlpatterns = router.urls
