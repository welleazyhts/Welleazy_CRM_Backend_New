from http import client
from rest_framework import serializers
from .models import CareProgram , EyeDentalTreatment , MedicalCamp , CampCase
from apps.test_individual.models import IndividualTest as Test

class CareProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareProgram
        fields = [
            'id',
            'care_program_name',
            'normal_price',
            'care_program_details',
            'image',
            'is_active',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'deleted_at'
        ]


# EYE & DENTAL TREATMENTS SERIALIZER-----

class EyeDentalTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeDentalTreatment
        fields = [
            "id",
            "treatment_type",
            "treatment_name",
            "image",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "deleted_at",
        ]


# MEDICAL CAMP SERIALIZER-----


class MedicalCampSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="main_client.corporate_name", read_only=True)
    sub_client_name = serializers.CharField(source="sub_client.name", read_only=True)
    package_name = serializers.CharField(source="package.package_name", read_only=True)
    test_name = serializers.CharField(source="tests.test_name", read_only=True)
    network_provider_name = serializers.CharField(source="network_provider.center_name", read_only=True)


    class Meta:
        model = MedicalCamp
        fields = "__all__"
        read_only_fields = ("case_id", "created_at")

    def validate(self, attrs):
        request_from = attrs.get("camp_request_from")
        main_client = attrs.get("main_client")
        sub_client = attrs.get("sub_client")
        package = attrs.get("package")
        test=attrs.get("tests")
        camp_status = attrs.get("camp_status")
        completed_count = attrs.get("completed_medical_count")

        if request_from == "Sub Client":
            if not sub_client:
                raise serializers.ValidationError(
                    "Sub client is required when request is from Sub Client."
                )
            if sub_client.client_id != main_client.id:
                raise serializers.ValidationError(
                    "Selected sub client does not belong to the selected main client."
                )
            
        
        if not main_client:
            raise serializers.ValidationError("Main client is required.")
        
        if not request_from:
            raise serializers.ValidationError("Camp request from is required.")
            
        if not package:
            raise serializers.ValidationError("Package is required.")
            
         # Package must belong to client
        if package and package.client_id != main_client.id:
            raise serializers.ValidationError("Selected package does not belong to the selected client.")

        # ✅ Test must belong to the selected package
        # Since Package has test_ids (M2M or reverse FK)
        if not package.tests_included.filter(id=test.id).exists():
            raise serializers.ValidationError("Selected test does not belong to the selected package.")
        

        if camp_status == "Completed":
            if completed_count is None:
                raise serializers.ValidationError(
                    "completed_medical_count is required when case_status is Completed."
                )
            if completed_count <= 0:
                raise serializers.ValidationError(
                    "completed_medical_count must be greater than 0 when case_status is Completed."
                )

        return attrs


# ADD CASE SERIALIZERS-----


class CampCaseSerializer(serializers.ModelSerializer):
    # Existing auto fields
    case__id = serializers.CharField(source="case_id", read_only=True)
    customer__id = serializers.CharField(source="customer_id", read_only=True)
    updated_by_name=serializers.CharField(source="updated_by.name", read_only=True)

    # ✅ Fields from MedicalCamp
    camp_id = serializers.CharField(source="camp.camp_id", read_only=True)
    client_name = serializers.CharField(source="camp.main_client.corporate_name", read_only=True)
    sub_client_name = serializers.CharField(source="camp.sub_client.name", read_only=True)
    camp_location = serializers.CharField(source="camp.camp_location", read_only=True)
    city_name = serializers.CharField(source="camp.camp_city.name", read_only=True)


    # Optional: names for FK fields in Case
    gender_name = serializers.CharField(source="customer_gender.name", read_only=True)
    status_name = serializers.CharField(source="case_status.name", read_only=True)

    class Meta:
        model = CampCase
        fields = "__all__"
        read_only_fields = ("case_id", "customer_id", "created_at")
