from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiscellaneousProgramCaseViewSet

router = DefaultRouter()
router.register(r'cases', MiscellaneousProgramCaseViewSet, basename='misc_program_cases')

urlpatterns = [
    path('', include(router.urls)),
]
