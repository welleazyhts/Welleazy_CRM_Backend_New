from django_filters import rest_framework as filters
from .models import ClientCustomer

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class ClientCustomerFilter(filters.FilterSet):
    client = filters.NumberFilter(field_name='client__id')
    branch = NumberInFilter(field_name='branch__id', lookup_expr='in')
    branch_zone = filters.NumberFilter(field_name='branch__branch_zone__id')
    
    # UI labels alignment
    customer_id = filters.CharFilter(field_name='member_id', lookup_expr='icontains')
    customer_name = filters.CharFilter(lookup_expr='icontains')
    customer_email_id = filters.CharFilter(field_name='email_id', lookup_expr='icontains')
    customer_mobile_number = filters.CharFilter(field_name='mobile_no', lookup_expr='icontains')
    
    status = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = ClientCustomer
        fields = [
            'client', 'branch', 'branch_zone', 
            'customer_id', 'customer_name', 
            'customer_email_id', 
            'customer_mobile_number', 
            'status'
        ]
