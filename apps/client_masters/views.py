from rest_framework import viewsets, views, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import (
    BusinessType, CorporateType, Source, VisitType, PartnershipStatus,
    ClientAgreementFrom, PaymentFrequency, Designation, WelleazyCRM, MemberRelationType,
    BranchZone, EmailNotificationType
)
from .serializers import (
    BusinessTypeSerializer, CorporateTypeSerializer, SourceSerializer,
    VisitTypeSerializer, PartnershipStatusSerializer, ClientAgreementFromSerializer,
    PaymentFrequencySerializer, DesignationSerializer, WelleazyCRMSerializer, MemberRelationTypeSerializer,
    BranchZoneSerializer, EmailNotificationTypeSerializer
)
from apps.accounts.models import User

class BaseMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name']

class BusinessTypeViewSet(BaseMasterViewSet):
    queryset = BusinessType.objects.all().order_by('name')
    serializer_class = BusinessTypeSerializer

class CorporateTypeViewSet(BaseMasterViewSet):
    queryset = CorporateType.objects.all().order_by('name')
    serializer_class = CorporateTypeSerializer

class SourceViewSet(BaseMasterViewSet):
    queryset = Source.objects.all().order_by('name')
    serializer_class = SourceSerializer

class VisitTypeViewSet(BaseMasterViewSet):
    queryset = VisitType.objects.all().order_by('name')
    serializer_class = VisitTypeSerializer

class PartnershipStatusViewSet(BaseMasterViewSet):
    queryset = PartnershipStatus.objects.all().order_by('name')
    serializer_class = PartnershipStatusSerializer

class ClientAgreementFromViewSet(BaseMasterViewSet):
    queryset = ClientAgreementFrom.objects.all().order_by('name')
    serializer_class = ClientAgreementFromSerializer

class PaymentFrequencyViewSet(BaseMasterViewSet):
    queryset = PaymentFrequency.objects.all().order_by('name')
    serializer_class = PaymentFrequencySerializer

class DesignationViewSet(BaseMasterViewSet):
    queryset = Designation.objects.all().order_by('name')
    serializer_class = DesignationSerializer

class WelleazyCRMViewSet(BaseMasterViewSet):
    queryset = WelleazyCRM.objects.all().order_by('name')
    serializer_class = WelleazyCRMSerializer

class MemberRelationTypeViewSet(BaseMasterViewSet):
    queryset = MemberRelationType.objects.all().order_by('name')
    serializer_class = MemberRelationTypeSerializer

class BranchZoneViewSet(BaseMasterViewSet):
    queryset = BranchZone.objects.all().order_by('name')
    serializer_class = BranchZoneSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class EmailNotificationTypeViewSet(BaseMasterViewSet):
    queryset = EmailNotificationType.objects.all().order_by('name')
    serializer_class = EmailNotificationTypeSerializer

class DropdownsAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "business_types": BusinessTypeSerializer(BusinessType.objects.filter(active=True), many=True).data,
            "corporate_types": CorporateTypeSerializer(CorporateType.objects.filter(active=True), many=True).data,
            "sources": SourceSerializer(Source.objects.filter(active=True), many=True).data,
            "visit_types": VisitTypeSerializer(VisitType.objects.filter(active=True), many=True).data,
            "partnership_statuses": PartnershipStatusSerializer(PartnershipStatus.objects.filter(active=True), many=True).data,
            "client_agreement_froms": ClientAgreementFromSerializer(ClientAgreementFrom.objects.filter(active=True), many=True).data,
            "payment_frequencies": PaymentFrequencySerializer(PaymentFrequency.objects.filter(active=True), many=True).data,
            "designations": DesignationSerializer(Designation.objects.filter(active=True), many=True).data,
            "welleazy_crms": WelleazyCRMSerializer(WelleazyCRM.objects.filter(active=True), many=True).data,
            "member_relation_types": MemberRelationTypeSerializer(MemberRelationType.objects.filter(active=True), many=True).data,
            "branch_zones": BranchZoneSerializer(BranchZone.objects.filter(active=True), many=True).data,
            "email_notification_types": EmailNotificationTypeSerializer(EmailNotificationType.objects.filter(active=True), many=True).data,
        }
        return Response(data)
