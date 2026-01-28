from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientBranchViewSet

router = DefaultRouter()
router.register(r'', ClientBranchViewSet, basename='client-branches')

urlpatterns = [
    path('', include(router.urls)),
]
