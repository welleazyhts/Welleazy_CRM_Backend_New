from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientCustomerViewSet

router = DefaultRouter()
router.register(r'', ClientCustomerViewSet, basename='client-customer')

urlpatterns = [
    path('', include(router.urls)),
]
