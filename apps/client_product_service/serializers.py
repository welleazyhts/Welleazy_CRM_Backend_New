from rest_framework import serializers
from .models import ClientProductService
from apps.master_management.models import MasterProductSubCategory

class ClientProductServiceSerializer(serializers.ModelSerializer):
    login_type_name = serializers.CharField(source='login_type.name', read_only=True)
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    
    services_details = serializers.SerializerMethodField()

    class Meta:
        model = ClientProductService
        fields = [
            'id', 'login_type', 'login_type_name', 
            'client', 'client_name', 
            'branch', 'branch_name', 
            'product', 'product_name', 
            'services', 'services_details',
            'is_active', 'created_at', 'updated_at',
            'created_by', 'created_by_name',
            'updated_by', 'updated_by_name'
        ]

    def get_services_details(self, obj):
        return [
            {'id': service.id, 'name': service.name} 
            for service in obj.services.all()
        ]

    def validate(self, attrs):
        client = attrs.get('client')
        branch = attrs.get('branch')
        product = attrs.get('product')
        services = attrs.get('services', [])
        
        if branch and client and branch.client != client:
            raise serializers.ValidationError({
                "branch": f"The selected branch '{branch.branch_name}' does not belong to the client '{client.corporate_name}'."
            })
        
        if services and product:
            from apps.master_management.models import ServiceMapping
            
            mapping = ServiceMapping.objects.filter(product=product).first()
            if not mapping:
                raise serializers.ValidationError({
                    "product": f"No service mapping found for product '{product.name}'."
                })
            
            valid_service_ids = set(mapping.sub_products.values_list('id', flat=True))
            for service in services:
                if service.id not in valid_service_ids:
                    raise serializers.ValidationError({
                        "services": f"The service '{service.name}' is not mapped to product '{product.name}'."
                    })
        
        return attrs
