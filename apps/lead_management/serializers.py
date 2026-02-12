from rest_framework import serializers
from django.db import transaction
from .models import LeadSource, LeadStatus, Lead, IndividualClient, IndividualClientDependent, IndividualClientDocument
from apps.master_management.models import State, City, MasterTypeOfInsurance, MasterInsuranceCompany, MasterRelationship
from apps.core.choices import GENDER_CHOICES

class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSource
        fields = '__all__'


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadStatus
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='lead_source.name', read_only=True)
    status_name = serializers.CharField(source='lead_status.name', read_only=True)

    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if obj.lead_type == 'Individual':
            return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        return obj.company_name or ''

    class Meta:
        model = Lead
        fields = '__all__'


class LeadPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def validate(self, data):
        if data.get('lead_type') == 'Individual' and not data.get('gender'):
            raise serializers.ValidationError({
                'gender': 'Gender is required for individual leads.'
            })
        return data


class IndividualClientDependentSerializer(serializers.ModelSerializer):
    relationship_name = serializers.CharField(source='relationship.name', read_only=True)


    class Meta:
        model = IndividualClientDependent
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


class IndividualClientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualClientDocument
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


class IndividualClientSerializer(serializers.ModelSerializer):
    dependents = IndividualClientDependentSerializer(many=True, read_only=True)
    documents = IndividualClientDocumentSerializer(many=True, read_only=True)
    
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    type_of_insurance_name = serializers.CharField(source='type_of_insurance.name', read_only=True)
    current_insurer_name = serializers.CharField(source='current_insurer.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = IndividualClient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


# Payload Serializers for Workflow Pattern
class IndividualClientDependentPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True)
    relationship = serializers.PrimaryKeyRelatedField(
        queryset=MasterRelationship.objects.all(), 
        required=False, 
        allow_null=True
    )
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False, allow_null=True)
    email_id = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    age = serializers.IntegerField(required=False, allow_null=True)


class IndividualClientDocumentPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)


class IndividualClientPayloadSerializer(serializers.Serializer):
    employee_name = serializers.CharField(required=True)
    employee_id = serializers.CharField(required=True)
    contact_no = serializers.CharField(required=True)
    company_email = serializers.EmailField(required=True)
    company_name = serializers.CharField(required=True)
    company_address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), required=False, allow_null=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False, allow_null=True)
    
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    type_of_insurance = serializers.PrimaryKeyRelatedField(
        queryset=MasterTypeOfInsurance.objects.all(), 
        required=False, 
        allow_null=True
    )
    current_insurer = serializers.PrimaryKeyRelatedField(
        queryset=MasterInsuranceCompany.objects.all(), 
        required=False, 
        allow_null=True
    )
    
    expiry_date = serializers.DateField(required=False, allow_null=True)
    premium_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    sum_assured = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(choices=IndividualClient.STATUS_CHOICES, default='Active')
    
    dependents = IndividualClientDependentPayloadSerializer(many=True, required=False)
    documents = IndividualClientDocumentPayloadSerializer(many=True, required=False)
