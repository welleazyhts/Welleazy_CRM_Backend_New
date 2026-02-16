from rest_framework import serializers
from .models import ClientCustomer, ClientCustomerAddress, ClientCustomerDependent
from apps.master_management.models import MasterProduct, MasterProductSubCategory, State, City, MasterRelationship
from apps.client.models import Client
from apps.client_branch.models import ClientBranch

class ClientCustomerAddressSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    relation_type_name = serializers.CharField(source='relation_type.name', read_only=True)

    class Meta:
        model = ClientCustomerAddress
        fields = '__all__'
        read_only_fields = ('customer',)

    def validate(self, attrs):
        city = attrs.get('city')
        state = attrs.get('state')
        
        # Validate city belongs to state
        if city and state and city.state != state:
            raise serializers.ValidationError({
                "city": f"The selected city '{city.name}' does not belong to the state '{state.name}'."
            })
        
        return attrs

class ClientCustomerDependentSerializer(serializers.ModelSerializer):
    relationship_name = serializers.CharField(source='relationship.name', read_only=True)

    class Meta:
        model = ClientCustomerDependent
        fields = '__all__'
        read_only_fields = ('customer',)

class ClientCustomerSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    
    addresses = ClientCustomerAddressSerializer(many=True, read_only=True)
    dependents = ClientCustomerDependentSerializer(many=True, read_only=True)
    
    services_details = serializers.SerializerMethodField()
    package_details = serializers.SerializerMethodField()

    class Meta:
        model = ClientCustomer
        fields = '__all__'
        read_only_fields = ('member_id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'created_by_name', 'updated_by_name')

    def get_services_details(self, obj):
        return [
            {'id': service.id, 'name': service.name}
            for service in obj.services.all()
        ]

    def get_package_details(self, obj):
        return [
            {'id': package.id, 'name': package.package_name}
            for package in obj.packages.all()
        ]

    def validate(self, attrs):
        client = attrs.get('client')
        branch = attrs.get('branch')
        city = attrs.get('city')
        state = attrs.get('state')
        product = attrs.get('product')
        services = attrs.get('services', [])
        
        if branch and client and branch.client != client:
            raise serializers.ValidationError({
                "branch": f"The selected branch '{branch.branch_name}' does not belong to the client '{client.corporate_name}'."
            })
        
        if city and state and city.state != state:
            raise serializers.ValidationError({
                "city": f"The selected city '{city.name}' does not belong to the state '{state.name}'."
            })
        
        if product and client:
            from apps.client_product_service.models import ClientProductService
            
            client_has_product = ClientProductService.objects.filter(
                product=product,
                client=client,
                is_active=True
            ).exists()
            
            if not client_has_product:
                raise serializers.ValidationError({
                    "product": f"The product '{product.name}' is not mapped to client '{client.corporate_name}'."
                })
        
        if services and product:
            from apps.master_management.models import ServiceMapping
            
            mapping = ServiceMapping.objects.filter(product=product).first()
            if mapping:
                valid_service_ids = set(mapping.sub_products.values_list('id', flat=True))
                for service in services:
                    if service.id not in valid_service_ids:
                        raise serializers.ValidationError({
                            "services": f"The service '{service.name}' is not mapped to product '{product.name}'."
                        })
        
        return attrs
