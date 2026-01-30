from rest_framework import serializers

from .models import (
    PhysicalMedicalCase,
    PhysicalMedicalClientDetail,
    PhysicalMedicalCustomerDetail,
    PhysicalMedicalCaseDetail,
    PhysicalMedicalDependent
)

# =================================================
# DEPENDENT SERIALIZER
# =================================================
class PhysicalMedicalDependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalDependent
        fields = [
            "case_for",
            "dependent_name",
            "mobile_number",
            "gender",
            "date_of_birth",
            "address",
            "medical_test",
        ]


# =================================================
# CLIENT DETAIL SERIALIZER
# =================================================
class PhysicalMedicalClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalClientDetail
        fields = [
            "client",
            "client_branch",
            "customer_type",
            "product",
            "service_offered",
            "received_by_name",
            "received_mobile",
            "received_email",
            "department",
        ]


# =================================================
# CUSTOMER DETAIL SERIALIZER
# =================================================
class PhysicalMedicalCustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalCustomerDetail
        fields = [
            "customer_name",
            "mobile_number",
            "alternate_number",
            "gender",
            "email_id",
            "state",
            "city",
            "pincode",
            "address",
            "area_locality",
            "landmark",
            "date_of_birth",
            "geo_location",
        ]


# =================================================
# CASE DETAIL SERIALIZER
# =================================================
class PhysicalMedicalCaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMedicalCaseDetail
        fields = [
            "medical_test",
            "generic_test",
            "customer_profile",
            "application_no",
            "case_type",
            "payment_type",
            "case_for",
            "dhoc_payment",
            "customer_pay_amount",
            "preferred_visit_type",
            "preferred_appointment_datetime",
            "company_name",
        ]


# =================================================
# CASE DETAIL (FULL VIEW / CREATE RESPONSE)
# =================================================
class PhysicalMedicalCaseSerializer(serializers.ModelSerializer):

    client_detail = PhysicalMedicalClientDetailSerializer(read_only=True)
    customer_detail = PhysicalMedicalCustomerDetailSerializer(read_only=True)
    case_detail = PhysicalMedicalCaseDetailSerializer(read_only=True)
    dependents = PhysicalMedicalDependentSerializer(many=True, read_only=True)

    class Meta:
        model = PhysicalMedicalCase
        fields = [
            "id",
            "case_id",
            "case_received_mode",
            "case_received_datetime",
            "case_status",
            "client_detail",
            "customer_detail",
            "case_detail",
            "dependents",
            "created_at",
            "updated_at",
            
        ]


# =================================================
# CASE LIST SERIALIZER (LIST API)
# =================================================
class PhysicalMedicalCaseListSerializer(serializers.ModelSerializer):

    client_name = serializers.CharField(
        source="client_detail.client.corporate_name",
        read_only=True
    )
    customer_name = serializers.CharField(
        source="customer_detail.customer_name",
        read_only=True
    )

    class Meta:
        model = PhysicalMedicalCase
        fields = [
            "id",
            "case_id",
            "client_name",
            "customer_name",
            "case_status",
            "case_received_datetime",
        ]
