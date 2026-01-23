from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("partnership-types", PartnershipTypeViewSet)
router.register("specialty-types", SpecialtyTypeViewSet)
router.register("ownership-types", OwnershipTypeViewSet)
router.register("service-categories", ServiceCategoryViewSet)
router.register("radiology-types", RadiologyTypeViewSet)
router.register("discount-services", DiscountServiceViewSet)
router.register("voucher-discount-types", VoucherDiscountTypeViewSet)
router.register("dc-unique-names", DCUniqueNameViewSet)
router.register("payment-terms", PaymentTermViewSet)

urlpatterns = router.urls
