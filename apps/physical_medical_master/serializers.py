from rest_framework import serializers
from .models import (
    CaseReceivedMode,
    CaseType,
    PaymentType,
    CaseFor,
    PreferredVisitType,
    CaseStatus,
    CustomerType,
    ServiceOffered,
    
    MedicalTest,
    
    CustomerProfile,
    DhocPaymentOption,
)

# 🔹 COMMON BASE SERIALIZER
class BaseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "is_active"]
class CaseReceivedModeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = CaseReceivedMode


class CaseTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = CaseType


class PaymentTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = PaymentType


class CaseForSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = CaseFor


class PreferredVisitTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = PreferredVisitType


class CaseStatusSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = CaseStatus

class CustomerTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = CustomerType


class ServiceOfferedSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = ServiceOffered





class MedicalTestSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = MedicalTest




class CustomerProfileSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = CustomerProfile


class DhocPaymentOptionSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = DhocPaymentOption
