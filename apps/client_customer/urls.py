from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientCustomerViewSet

router = DefaultRouter()
router.register(r'client-customers', ClientCustomerViewSet, basename='client-customer')

urlpatterns = [
    path('', include(router.urls)),
]
