from rest_framework import serializers
from .models import SubClient, SubClientSPOC
from apps.client.models import Client
from apps.client.serializers import ClientSerializer
from apps.client_masters.models import Designation
from django.db import transaction
import json

class SubClientSPOCSerializer(serializers.ModelSerializer):
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = SubClientSPOC
        fields = ['id', 'name', 'contact_no', 'mobile_no', 'email_id', 'designation', 'designation_name']

class SubClientSPOCPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True)
    contact_no = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    email_id = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(),
        required=False,
        allow_null=True
    )

class SubClientSerializer(serializers.ModelSerializer):
    spocs = SubClientSPOCPayloadSerializer(many=True, required=False)
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    corporate_type_name = serializers.CharField(source='corporate_type.name', read_only=True)

    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = SubClient
        fields = [
            'id', 'client', 'client_name', 'name', 'corporate_type', 'corporate_type_name',
            'mobile_no', 'landline_no', 'email_id',
            'head_office_address', 'branch_office_address',
            'source', 'lead_by', 'is_active',
            'spocs', 'created_at', 'updated_at', 
            'created_by', 'created_by_name', 'updated_by', 'updated_by_name'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['spocs'] = SubClientSPOCSerializer(instance.spocs.all(), many=True).data
        return ret
