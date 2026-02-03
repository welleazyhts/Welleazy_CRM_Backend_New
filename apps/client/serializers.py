from rest_framework import serializers
from .models import Client, ClientSPOC, ClientDocument, EmailNotificationType
from apps.client_masters.models import (
    BusinessType, CorporateType, Source, VisitType, PartnershipStatus,
    ClientAgreementFrom, PaymentFrequency, Designation, WelleazyCRM, MemberRelationType
)
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
        read_only_fields = ['corporate_code']

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


class ClientSPOCPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)

    person_name = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=True)
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(),
        required=False,
        allow_null=True
    )
    contact_no = serializers.CharField(required=False, allow_null=True)
    email_id = serializers.EmailField(required=True)

    receive_email_for = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=EmailNotificationType.objects.all(),
        required=False
    )

class ClientDocumentPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)

class ClientPayloadSerializer(serializers.Serializer):

    # Business Info
    business_type = serializers.PrimaryKeyRelatedField(queryset=BusinessType.objects.all(), required=False, allow_null=True)
    corporate_code = serializers.CharField(required=False, allow_blank=True, read_only=True)
    corporate_name = serializers.CharField(required=False, allow_blank=True)
    corporate_type = serializers.PrimaryKeyRelatedField(queryset=CorporateType.objects.all(), required=False, allow_null=True)

    # Contact Info
    mobile_no = serializers.CharField(required=False, allow_blank=True)
    landline_no = serializers.CharField(required=False, allow_null=True)
    email_id = serializers.EmailField(required=False, allow_blank=True)

    # Address Info
    head_office_address = serializers.CharField(required=False, allow_blank=True)
    branch_office_address = serializers.CharField(required=False, allow_null=True)

    # Sales/Ops Info
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), required=False, allow_null=True)
    referred_by = serializers.CharField(required=False, allow_null=True)
    welleazy_crm = serializers.PrimaryKeyRelatedField(queryset=WelleazyCRM.objects.all(), required=False, allow_null=True)
    sales_manager = serializers.CharField(required=False, allow_blank=True)
    broker = serializers.CharField(required=False, allow_blank=True)
    ops_spoc = serializers.CharField(required=False, allow_blank=True)

    # Financial / Legal
    service_charges = serializers.CharField(required=False, allow_null=True)
    pan_no = serializers.CharField(required=False, allow_null=True)
    gst_no = serializers.CharField(required=False, allow_null=True)
    home_visit_charges = serializers.CharField(required=False, allow_null=True)
    account_id = serializers.CharField(required=False, allow_null=True)
    channel_partner_id = serializers.CharField(required=False, allow_null=True)

    # Other
    website_url = serializers.URLField(required=False, allow_null=True)
    billing_email_address = serializers.EmailField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)

    # Sponsorship
    total_sponsored = serializers.CharField(required=False, allow_null=True)
    total_non_sponsored = serializers.CharField(required=False, allow_null=True)
    is_dependent_sponsored = serializers.BooleanField(required=False)
    members_sponsored = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MemberRelationType.objects.all(),
        required=False
    )

    case_registration_mail_auto_triggered = serializers.BooleanField(required=False)
    separate_access = serializers.BooleanField(required=False)

    # Visit / Partnership
    visit_type = serializers.PrimaryKeyRelatedField(queryset=VisitType.objects.all(), required=False, allow_null=True)
    corporate_partnership_status = serializers.PrimaryKeyRelatedField(queryset=PartnershipStatus.objects.all(), required=False, allow_null=True)

    # Agreement
    client_agreement_from = serializers.PrimaryKeyRelatedField(queryset=ClientAgreementFrom.objects.all(), required=False, allow_null=True)
    agreement_date = serializers.DateField(required=False, allow_null=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    frequency_of_payment = serializers.PrimaryKeyRelatedField(queryset=PaymentFrequency.objects.all(), required=False, allow_null=True)

    spocs = ClientSPOCPayloadSerializer(many=True, required=False)

    documents = ClientDocumentPayloadSerializer(many=True, required=False)

