from rest_framework import serializers
from .models import (
    BusinessType, CorporateType, Source, VisitType, PartnershipStatus,
    ClientAgreementFrom, PaymentFrequency, Designation, WelleazyCRM, MemberRelationType,
    BranchZone, EmailNotificationType
)

class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'active', 'created_at', 'updated_at']

class BusinessTypeSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = BusinessType

class CorporateTypeSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = CorporateType

class SourceSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = Source

class VisitTypeSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = VisitType

class PartnershipStatusSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = PartnershipStatus

class ClientAgreementFromSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = ClientAgreementFrom

class PaymentFrequencySerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = PaymentFrequency

class DesignationSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = Designation

class WelleazyCRMSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = WelleazyCRM

class MemberRelationTypeSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = MemberRelationType

class BranchZoneSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = BranchZone

class EmailNotificationTypeSerializer(MasterSerializer):
    class Meta(MasterSerializer.Meta):
        model = EmailNotificationType

