from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareProgramViewSet

router = DefaultRouter()
router.register(r'care-programs', CareProgramViewSet, basename='care-programs')

urlpatterns = [
    path('', include(router.urls)),
]
