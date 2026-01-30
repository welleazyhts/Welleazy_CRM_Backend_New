from django_filters import rest_framework as filters
from .models import ClientCustomer

class ClientCustomerFilter(filters.FilterSet):
    client = filters.NumberFilter(field_name='client__id')
    branch = filters.NumberFilter(field_name='branch__id')
    branch_zone = filters.NumberFilter(field_name='branch__branch_zone__id')
    
    customer_id = filters.CharFilter(field_name='member_id', lookup_expr='icontains')
    member_id = filters.CharFilter(lookup_expr='icontains')
    customer_name = filters.CharFilter(lookup_expr='icontains')
    customer_email_id = filters.CharFilter(field_name='email_id', lookup_expr='icontains')
    email_id = filters.CharFilter(lookup_expr='icontains')
    customer_mobile_number = filters.CharFilter(field_name='mobile_no', lookup_expr='icontains')
    mobile_no = filters.CharFilter(lookup_expr='icontains')
    
    status = filters.BooleanFilter(field_name='is_active')
    is_active = filters.BooleanFilter()

    class Meta:
        model = ClientCustomer
        fields = [
            'client', 'branch', 'branch_zone', 
            'customer_id', 'member_id', 'customer_name', 
            'customer_email_id', 'email_id', 
            'customer_mobile_number', 'mobile_no', 
            'status', 'is_active'
        ]
