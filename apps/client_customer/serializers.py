from rest_framework import serializers
from .models import ClientCustomer
# from apps.test_package.models import TestPackage
from apps.master_management.models import MasterProduct, MasterProductSubCategory
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.master_management.models import State, City

class ClientCustomerSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    
    # Custom fields for M2M details
    services_details = serializers.SerializerMethodField()
    packages_details = serializers.SerializerMethodField()

    class Meta:
        model = ClientCustomer
        fields = '__all__'
        read_only_fields = ('member_id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'created_by_name', 'updated_by_name')

    def get_services_details(self, obj):
        return [
            {'id': service.id, 'name': service.name}
            for service in obj.services.all()
        ]

    def get_packages_details(self, obj):
        return [
            {'id': package.id, 'name': package.package_name}
            for package in obj.packages.all()
        ]

    def validate(self, data):
        return data
