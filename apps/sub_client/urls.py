from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubClientViewSet

router = DefaultRouter()
router.register(r'', SubClientViewSet, basename='sub-clients')

urlpatterns = [
    path('', include(router.urls)),
]
