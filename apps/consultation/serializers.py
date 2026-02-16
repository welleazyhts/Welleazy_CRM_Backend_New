from rest_framework import serializers
from .models import ConsultationCase, ConsultationDoctorDetails, ConsultationCaseDependent, ConsultationCaseDocument
from apps.master_management.models import MasterProduct, MasterProductSubCategory, MasterBranch, State, City, MasterLanguage, MasterRelationship, CaseStatus, MasterSpecialtiesTest
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.accounts.models import User
from apps.doctor.models import Doctor
from apps.client_product_service.models import ClientProductService

class ConsultationDoctorDetailsSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.doctor_name', read_only=True)
    preferred_language_name = serializers.CharField(source='preferred_language.name', read_only=True)
    case_status_name = serializers.CharField(source='case_status.name', read_only=True)

    class Meta:
        model = ConsultationDoctorDetails
        fields = '__all__'
        read_only_fields = ('case',)

class ConsultationCaseDependentSerializer(serializers.ModelSerializer):
    relationship_name = serializers.CharField(source='relationship.name', read_only=True)
    preferred_language_name = serializers.CharField(source='preferred_language.name', read_only=True)

    class Meta:
        model = ConsultationCaseDependent
        fields = '__all__'
        read_only_fields = ('case',)

class ConsultationCaseDocumentSerializer(serializers.ModelSerializer):
    document_file = serializers.FileField(required=False)
    class Meta:
        model = ConsultationCaseDocument
        fields = '__all__'
        read_only_fields = ('case',)

class ConsultationCaseSerializer(serializers.ModelSerializer):
    consultation_type_name = serializers.CharField(source='consultation_type.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    specialities_test_list_name = serializers.CharField(source='specialities_test_list.name', read_only=True)
    welleazy_branch_name = serializers.CharField(source='welleazy_branch.name', read_only=True)
    corporate_name_display = serializers.CharField(source='corporate_name.corporate_name', read_only=True)
    branch_name_display = serializers.CharField(source='branch_name.branch_name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    preferred_language_name = serializers.CharField(source='preferred_language.name', read_only=True)
    case_status_name = serializers.CharField(source='case_status.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    doctor_details = ConsultationDoctorDetailsSerializer(many=True, read_only=True)
    dependents = ConsultationCaseDependentSerializer(many=True, read_only=True)
    documents = ConsultationCaseDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ConsultationCase
        fields = '__all__'
        read_only_fields = ('case_id', 'created_at', 'updated_at', 'created_by', 'updated_by')

class ConsultationCasePayloadSerializer(serializers.ModelSerializer):
    dependents = ConsultationCaseDependentSerializer(many=True, required=False)
    documents = ConsultationCaseDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ConsultationCase
        fields = '__all__'
        read_only_fields = ('case_id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def validate(self, attrs):
        
        consultation_type = attrs.get('consultation_type')
        service = attrs.get('service')
        client = attrs.get('corporate_name')
        branch = attrs.get('branch_name')
        
        if branch and client and branch.client != client:
            raise serializers.ValidationError({
                "branch_name": f"The selected branch '{branch.branch_name}' does not belong to the client '{client.corporate_name}'."
            })
        
        if consultation_type and client:
            client_has_product = ClientProductService.objects.filter(
                product=consultation_type,
                client=client,
                is_active=True
            ).exists()
            
            if not client_has_product:
                raise serializers.ValidationError({
                    "corporate_name": f"The client '{client.corporate_name}' does not have the product '{consultation_type.name}' mapped in their services."
                })
        
        if service and consultation_type and client:
            client_product_services = ClientProductService.objects.filter(
                product=consultation_type,
                client=client,
                is_active=True
            ).prefetch_related('services')
            
            service_exists = False
            for cps in client_product_services:
                if cps.services.filter(id=service.id).exists():
                    service_exists = True
                    break
            
            if not service_exists:
                raise serializers.ValidationError({
                    "service": f"The service '{service.name}' is not mapped to product '{consultation_type.name}' for client '{client.corporate_name}'."
                })
        
        if branch and consultation_type and client:
            branch_has_product = ClientProductService.objects.filter(
                product=consultation_type,
                client=client,
                branch=branch,
                is_active=True
            ).exists()
            
            if not branch_has_product:
                raise serializers.ValidationError({
                    "branch_name": f"The branch '{branch.branch_name}' does not have the product '{consultation_type.name}' mapped."
                })
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('dependents', None)
        validated_data.pop('documents', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('dependents', None)
        validated_data.pop('documents', None)
        return super().update(instance, validated_data)


class ConsultationDoctorDetailsPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationDoctorDetails
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
