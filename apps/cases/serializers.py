from rest_framework import serializers
from .models import (
    Case,
    CaseServiceDetails,
    CaseFinancialDetails,
    CaseAdditionalDetails
)

# ===========================
# SERVICE DETAILS
# ===========================
class CaseServiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseServiceDetails
        fields = "__all__"
        extra_kwargs = {
            "case": {"read_only": True},
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
        }


# ===========================
# FINANCIAL DETAILS
# ===========================
class CaseFinancialDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseFinancialDetails
        fields = "__all__"
        extra_kwargs = {
            "case": {"read_only": True},
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
        }


# ===========================
# ADDITIONAL DETAILS
# ===========================
class CaseAdditionalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseAdditionalDetails
        fields = "__all__"
        extra_kwargs = {
            "case": {"read_only": True},
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
        }


# ===========================
# MAIN CASE SERIALIZER
# ===========================
class CaseSerializer(serializers.ModelSerializer):
    service = CaseServiceDetailsSerializer(required=False)
    financial = CaseFinancialDetailsSerializer(required=False)
    additional = CaseAdditionalDetailsSerializer(required=False)

    class Meta:
        model = Case
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
        }

    # -----------------------
    # CREATE
    # -----------------------
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        service_data = validated_data.pop("service", None)
        financial_data = validated_data.pop("financial", None)
        additional_data = validated_data.pop("additional", None)

        case = Case.objects.create(
            created_by=user,
            **validated_data
        )

        if service_data:
            CaseServiceDetails.objects.create(
                case=case,
                created_by=user,
                **service_data
            )

        if financial_data:
            CaseFinancialDetails.objects.create(
                case=case,
                created_by=user,
                **financial_data
            )

        if additional_data:
            CaseAdditionalDetails.objects.create(
                case=case,
                created_by=user,
                **additional_data
            )

        case.refresh_from_db()
        return case

    # -----------------------
    # UPDATE
    # -----------------------
    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        service_data = validated_data.pop("service", None)
        financial_data = validated_data.pop("financial", None)
        additional_data = validated_data.pop("additional", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.updated_by = user
        instance.save()

        if service_data:
            CaseServiceDetails.objects.update_or_create(
                case=instance,
                defaults={**service_data, "updated_by": user}
            )

        if financial_data:
            CaseFinancialDetails.objects.update_or_create(
                case=instance,
                defaults={**financial_data, "updated_by": user}
            )

        if additional_data:
            CaseAdditionalDetails.objects.update_or_create(
                case=instance,
                defaults={**additional_data, "updated_by": user}
            )

        instance.refresh_from_db()
        return instance
