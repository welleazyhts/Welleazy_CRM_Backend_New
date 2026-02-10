from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CHPViewSet, CampCaseViewSet, CareProgramViewSet, DentalTreatmentCaseViewSet, EyeDentalTreatmentViewSet, EyeTreatmentCaseViewSet, MedicalCampViewSet, TypeOfOHCViewSet , OHCViewSet

router = DefaultRouter()
router.register(r'care-programs', CareProgramViewSet, basename='care-programs')
router.register(r"eye-dental-treatments", EyeDentalTreatmentViewSet, basename="eye-dental-treatments")
router.register(r"medical-camps", MedicalCampViewSet, basename="medical-camps")
router.register(r"camp-cases", CampCaseViewSet, basename="camp-cases")
router.register(r"chp", CHPViewSet, basename="chp")
router.register(r"ohc-types", TypeOfOHCViewSet, basename="ohc-types")
router.register(r"ohc", OHCViewSet, basename="ohc")
router.register(r'eye-treatment-cases',EyeTreatmentCaseViewSet,basename='eye-treatment-cases')
router.register(r'dental-treatment-cases', DentalTreatmentCaseViewSet, basename='dental-treatment-cases')



urlpatterns = [
    path('', include(router.urls)),
]
