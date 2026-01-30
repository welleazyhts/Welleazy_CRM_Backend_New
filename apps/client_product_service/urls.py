from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientProductServiceViewSet

router = DefaultRouter()
router.register(r'', ClientProductServiceViewSet, basename='client-product-services')

urlpatterns = [
    path('', include(router.urls)),
]
