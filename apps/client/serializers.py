from rest_framework import serializers
from .models import Client, ClientSPOC, ClientDocument, EmailNotificationType
from apps.client_masters.serializers import (
    BusinessTypeSerializer, CorporateTypeSerializer, SourceSerializer,
    VisitTypeSerializer, PartnershipStatusSerializer, ClientAgreementFromSerializer,
    PaymentFrequencySerializer, DesignationSerializer, WelleazyCRMSerializer, MemberRelationTypeSerializer
)
from apps.accounts.models import User

class ClientSPOCSerializer(serializers.ModelSerializer):
    receive_email_for = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=EmailNotificationType.objects.all(),
        required=False
    )
    class Meta:
        model = ClientSPOC
        fields = ['id', 'person_name', 'mobile_no', 'designation', 'contact_no', 'email_id', 'receive_email_for']

class ClientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        exclude = ("created_by", "updated_by", "deleted_at")
        read_only_fields = ("id", "client")

class ClientSerializer(serializers.ModelSerializer):
    spocs = ClientSPOCSerializer(many=True, required=False)
    documents = ClientDocumentSerializer(many=True, read_only=True)
    
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        spocs_data = validated_data.pop('spocs', [])
        members_sponsored_data = validated_data.pop('members_sponsored', [])
        
        client = Client.objects.create(**validated_data)
        
        # Set ManyToMany fields
        if members_sponsored_data:
            client.members_sponsored.set(members_sponsored_data)
            
        # Create SPOCs
        for spoc_data in spocs_data:
            receive_email_for_data = spoc_data.pop('receive_email_for', [])
            spoc = ClientSPOC.objects.create(client=client, **spoc_data)
            if receive_email_for_data:
                spoc.receive_email_for.set(receive_email_for_data)
            
        return client

    def update(self, instance, validated_data):
        spocs_data = validated_data.pop('spocs', None)
        members_sponsored_data = validated_data.pop('members_sponsored', None)
        
        # Update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update ManyToMany fields
        if members_sponsored_data is not None:
            instance.members_sponsored.set(members_sponsored_data)
            
        # Update SPOCs
        if spocs_data is not None:
            instance.spocs.all().delete()
            for spoc_data in spocs_data:
                receive_email_for_data = spoc_data.pop('receive_email_for', [])
                spoc = ClientSPOC.objects.create(client=instance, **spoc_data)
                if receive_email_for_data:
                    spoc.receive_email_for.set(receive_email_for_data)
                
        return instance


class ClientPayloadSerializer(serializers.Serializer):
    # Business Info
    business_type = serializers.IntegerField(required=False, allow_null=True)
    corporate_code = serializers.CharField(required=False, allow_blank=True)
    corporate_name = serializers.CharField(required=False, allow_blank=True)
    corporate_type = serializers.IntegerField(required=False, allow_null=True)
    
    # Contact Info
    mobile_no = serializers.CharField(required=False, allow_blank=True)
    landline_no = serializers.CharField(required=False, allow_null=True)
    email_id = serializers.EmailField(required=False, allow_blank=True)
    
    # Address Info
    head_office_address = serializers.CharField(required=False, allow_blank=True)
    branch_office_addresses = serializers.CharField(required=False, allow_null=True)
    
    # Sales/Ops Info
    source = serializers.IntegerField(required=False, allow_null=True)
    referred_by = serializers.CharField(required=False, allow_null=True)
    welleazy_crm = serializers.IntegerField(required=False, allow_null=True)
    sales_manager = serializers.CharField(required=False, allow_blank=True)
    broker = serializers.CharField(required=False, allow_blank=True)
    ops_spoc = serializers.CharField(required=False, allow_blank=True)
    
    # Financial/Legal Info
    service_charges = serializers.CharField(required=False, allow_null=True)
    pan_no = serializers.CharField(required=False, allow_null=True)
    gst_no = serializers.CharField(required=False, allow_null=True)
    home_visit_charges = serializers.CharField(required=False, allow_null=True)
    account_id = serializers.CharField(required=False, allow_null=True)
    
    # Other Info
    channel_partner_id = serializers.CharField(required=False, allow_null=True)
    website_url = serializers.URLField(required=False, allow_null=True)
    billing_email_address = serializers.EmailField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False, default=True)
    
    # Sponsorship Info
    total_sponsored = serializers.CharField(required=False, allow_null=True)
    total_non_sponsored = serializers.CharField(required=False, allow_null=True)
    is_dependent_sponsored = serializers.BooleanField(required=False, default=False)
    members_sponsored = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    case_registration_mail_auto_triggered = serializers.BooleanField(required=False, default=False)
    separate_account = serializers.BooleanField(required=False, default=False)
    
    # Visit/Partnership
    visit_type = serializers.IntegerField(required=False, allow_null=True)
    corporate_partnership_status = serializers.IntegerField(required=False, allow_null=True)
    
    # Agreement
    client_agreement_from = serializers.IntegerField(required=False, allow_null=True)
    agreement_date = serializers.DateField(required=False, allow_null=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    frequency_of_payment = serializers.IntegerField(required=False, allow_null=True)
    
    # SPOCs
    spocs = serializers.ListField(child=serializers.DictField(), required=False, allow_empty=True)
    
    # Document management
    keep_documents = serializers.ListField(child=serializers.IntegerField(), required=False)
