from rest_framework import serializers
from .models import MiscellaneousProgramCase
from apps.master_management.serializers import (
    StateSerializer, CitySerializer, CaseStatusSerializer, MasterRelationshipSerializer
)
from apps.client.serializers import ClientSerializer
from apps.client_branch.serializers import ClientBranchSerializer
from apps.client_customer.serializers import ClientCustomerSerializer, ClientCustomerDependentSerializer

class MiscellaneousProgramCaseSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    employee_name = serializers.CharField(source='employee.customer_name', read_only=True)
    relationship_name = serializers.CharField(source='relationship.name', read_only=True)
    status_name = serializers.CharField(source='case_status.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    
    class Meta:
        model = MiscellaneousProgramCase
        fields = '__all__'
        read_only_fields = ('case_id', 'created_at', 'updated_at', 'created_by', 'updated_by')

class MiscellaneousProgramCasePayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscellaneousProgramCase
        fields = '__all__'
        read_only_fields = ('case_id', 'created_at', 'updated_at', 'created_by', 'updated_by')
        extra_kwargs = {
            'customer_name': {'required': False},
            'mobile_no': {'required': False},
            'email_id': {'required': False},
        }

    def validate(self, attrs):
        client = attrs.get('client')
        branch = attrs.get('branch')
        case_for = attrs.get('case_for')
        employee = attrs.get('employee')
        relationship_person = attrs.get('relationship_person')
        
        if branch and client and branch.client != client:
            raise serializers.ValidationError({
                "branch": f"The selected branch '{branch.branch_name}' does not belong to the client '{client.corporate_name}'."
            })

        if employee and client and employee.client != client:
            raise serializers.ValidationError({
                "employee": f"The employee '{employee.customer_name}' does not belong to the client '{client.corporate_name}'."
            })

        def get_address_str(customer, relation_type=None):
            from apps.client_customer.models import ClientCustomerAddress
            addr_qs = ClientCustomerAddress.objects.filter(customer=customer)
            if relation_type:
                addr = addr_qs.filter(relation_type=relation_type).first()
                if addr:
                    return f"{addr.address_line_1 or ''} {addr.address_line_2 or ''} {addr.area_locality or ''}".strip()
            
            addr = addr_qs.filter(is_default=True).first() or addr_qs.first()
            if addr:
                return f"{addr.address_line_1 or ''} {addr.address_line_2 or ''} {addr.area_locality or ''}".strip()
            return None

        if case_for and case_for.name.lower() == 'self':
            if not employee:
                raise serializers.ValidationError({"employee": "Employee is required for 'Self' cases."})
            
            attrs.setdefault('customer_name', employee.customer_name)
            attrs.setdefault('mobile_no', employee.mobile_no)
            attrs.setdefault('email_id', employee.email_id)
            attrs.setdefault('address', get_address_str(employee, case_for))
            attrs['relationship_person'] = None
            
        elif case_for:
            if relationship_person:
                if relationship_person.customer != employee:
                    raise serializers.ValidationError({
                        "relationship_person": f"The dependent '{relationship_person.name}' is not registered under employee '{employee.customer_name}'."
                    })
                
                attrs.setdefault('customer_name', relationship_person.name)
                attrs.setdefault('mobile_no', relationship_person.mobile_no or (employee.mobile_no if employee else None))
                attrs.setdefault('email_id', relationship_person.email_id or (employee.email_id if employee else None))
                attrs.setdefault('address', get_address_str(employee, case_for))
            else:
                if not attrs.get('customer_name') or not attrs.get('mobile_no'):
                    raise serializers.ValidationError({
                        "non_field_errors": "Please either select a 'Relationship Person' or manually provide 'customer_name' and 'mobile_no'."
                    })
            
        return attrs
