from rest_framework import serializers
from .models import SubClient, SubClientSPOC
from apps.client.models import Client
from apps.client.serializers import ClientSerializer
from django.db import transaction
import json

class SubClientSPOCSerializer(serializers.ModelSerializer):
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = SubClientSPOC
        fields = ['id', 'name', 'contact_no', 'mobile_no', 'email_id', 'designation', 'designation_name']

class SubClientSerializer(serializers.ModelSerializer):
    spocs = SubClientSPOCSerializer(many=True, required=False)
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

    @transaction.atomic
    def create(self, validated_data):
        spocs_data = validated_data.pop('spocs', [])
        sub_client = SubClient.objects.create(**validated_data)
        
        for spoc_data in spocs_data:
            SubClientSPOC.objects.create(sub_client=sub_client, **spoc_data)
            
        return sub_client

    @transaction.atomic
    def update(self, instance, validated_data):
        spocs_data = validated_data.pop('spocs', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if spocs_data:
            for spoc_data in spocs_data:
                SubClientSPOC.objects.create(sub_client=instance, **spoc_data)
                
        return instance
