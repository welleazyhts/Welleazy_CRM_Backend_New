from rest_framework import serializers
from .models import (
    PhysicalMedicalCase,
    PhysicalMedicalClientDetail,
    PhysicalMedicalCustomerDetail,
    PhysicalMedicalCaseDetail
)

class PhysicalMedicalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalCase
        fields = "__all__"


class PhysicalMedicalClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalClientDetail
        fields = "__all__"


class PhysicalMedicalCustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalCustomerDetail
        fields = "__all__"


class PhysicalMedicalCaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalCaseDetail
        fields = "__all__"


class PhysicalMedicalAddCaseSerializer(serializers.Serializer):
    case = PhysicalMedicalCaseSerializer()
    client = PhysicalMedicalClientDetailSerializer()
    customer = PhysicalMedicalCustomerDetailSerializer()
    case_detail = PhysicalMedicalCaseDetailSerializer()
