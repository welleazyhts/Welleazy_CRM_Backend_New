from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationCaseViewSet, ConsultationDoctorDetailsViewSet

router = DefaultRouter()
router.register(r'cases', ConsultationCaseViewSet)
router.register(r'doctor-appointments', ConsultationDoctorDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
