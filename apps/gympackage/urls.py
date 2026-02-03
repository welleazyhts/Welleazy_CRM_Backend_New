from rest_framework.routers import DefaultRouter
from .views import GymPackageViewSet , PackagePriceViewSet

router = DefaultRouter()


# MASTER TABLE URLS----

router.register(r'package-price-types', PackagePriceViewSet, basename='package-prices')

#MAIN TABLE URLS----

router.register(r"gym-packages", GymPackageViewSet, basename='gym-packages')

urlpatterns = router.urls