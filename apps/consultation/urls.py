from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationCaseViewSet

router = DefaultRouter()
router.register(r'cases', ConsultationCaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
