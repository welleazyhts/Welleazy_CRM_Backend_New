from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessTypeViewSet, CorporateTypeViewSet, SourceViewSet, VisitTypeViewSet,
    PartnershipStatusViewSet, ClientAgreementFromViewSet, PaymentFrequencyViewSet,
    DesignationViewSet, WelleazyCRMViewSet, MemberRelationTypeViewSet, DropdownsAPIView,
    BranchZoneViewSet, EmailNotificationTypeViewSet
)

router = DefaultRouter()
router.register(r'business-types', BusinessTypeViewSet)
router.register(r'corporate-types', CorporateTypeViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'visit-types', VisitTypeViewSet)
router.register(r'partnership-statuses', PartnershipStatusViewSet)
router.register(r'client-agreement-froms', ClientAgreementFromViewSet)
router.register(r'payment-frequencies', PaymentFrequencyViewSet)
router.register(r'designations', DesignationViewSet)
router.register(r'welleazy-crms', WelleazyCRMViewSet)
router.register(r'member-relation-types', MemberRelationTypeViewSet)
router.register(r'branch-zones', BranchZoneViewSet)
router.register(r'email-notification-types', EmailNotificationTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dropdowns/', DropdownsAPIView.as_view(), name='client-masters-dropdowns'),
]
