from rest_framework import serializers
from .models import DiagnosticCenter, DiagnosticLocation , DiagnosticServices , DiagnosticLabCapabilities , DiagnosticAccreditation , DiagnosticStaff , DiagnosticAgreement , DiagnosticBanking


# Location Serializer
class DiagnosticLocationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    class Meta:
        model = DiagnosticLocation
        exclude = ("center",)

# Service Serializer
class DiagnosticServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticServices
        exclude = ("center",)     

# Lab Capabilities Serializer

class DiagnosticLabCapabilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticLabCapabilities
        exclude = ("center",)


# Staff Serializer

class DiagnosticStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticStaff
        exclude = ("center",)

    
# Accreditation Serializer

class DiagnosticAccreditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticAccreditation
        exclude = ("center",)

# Banking Serializer


class DiagnosticBankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticBanking
        exclude = ("center",)

# Agreement Serializer


class DiagnosticAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticAgreement
        exclude = ("center",)

   

# Master Diagnostic Center Serializer


class DiagnosticCenterSerializer(serializers.ModelSerializer):
    location = DiagnosticLocationSerializer()
    services = DiagnosticServicesSerializer(source="diagnosticservices")
    lab_capabilities = DiagnosticLabCapabilitiesSerializer(source="diagnosticlabcapabilities")
    staff = DiagnosticStaffSerializer()
    accreditation = DiagnosticAccreditationSerializer(source="diagnosticaccreditation")
    banking = DiagnosticBankingSerializer(source="diagnosticbanking")
    agreement = DiagnosticAgreementSerializer()

    class Meta:
        model = DiagnosticCenter
        fields = "__all__"

    