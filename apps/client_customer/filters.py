from django_filters import rest_framework as filters
from .models import ClientCustomer

class ClientCustomerFilter(filters.FilterSet):
    client = filters.NumberFilter(field_name='client__id')
    branch = filters.NumberFilter(field_name='branch__id')
    branch_zone = filters.NumberFilter(field_name='branch__branch_zone__id')
    
    member_id = filters.CharFilter(lookup_expr='icontains')
    customer_name = filters.CharFilter(lookup_expr='icontains')
    email_id = filters.CharFilter(lookup_expr='icontains')
    mobile_no = filters.CharFilter(lookup_expr='icontains')
    
    is_active = filters.BooleanFilter()

    class Meta:
        model = ClientCustomer
        fields = [
            'client', 'branch', 'branch_zone', 
            'member_id', 'customer_name', 'email_id', 'mobile_no', 
            'is_active'
        ]
