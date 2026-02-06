from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampCaseViewSet, CareProgramViewSet, EyeDentalTreatmentViewSet, MedicalCampViewSet

router = DefaultRouter()
router.register(r'care-programs', CareProgramViewSet, basename='care-programs')
router.register(r"eye-dental-treatments", EyeDentalTreatmentViewSet, basename="eye-dental-treatments")
router.register(r"medical-camps", MedicalCampViewSet, basename="medical-camps")
router.register(r"camp-cases", CampCaseViewSet, basename="camp-cases")


urlpatterns = [
    path('', include(router.urls)),
]
