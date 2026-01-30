from rest_framework import serializers
from .models import ClientBranch
from django.db import transaction

class ClientBranchSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_zone_name = serializers.CharField(source='branch_zone.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = ClientBranch
        fields = [
            'id', 'client', 'client_name', 'branch_name', 'spoc_name', 
            'mobile_no', 'email_id', 'branch_zone', 'branch_zone_name',
            'state', 'state_name', 'city', 'city_name', 'address', 
            'is_active', 'created_at', 'updated_at',
            'created_by', 'created_by_name', 'updated_by', 'updated_by_name'
        ]
