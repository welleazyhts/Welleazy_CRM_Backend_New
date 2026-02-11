from django_filters import rest_framework as filters
from .models import ClientBranch
from apps.core.filters import NumberInFilter

class ClientBranchFilter(filters.FilterSet):
    client = NumberInFilter(field_name='client__id', lookup_expr='in')
    branch_name = filters.CharFilter(lookup_expr='icontains')
    email_id = filters.CharFilter(lookup_expr='icontains')
    mobile_no = filters.CharFilter(lookup_expr='icontains')
    branch_zone = NumberInFilter(field_name='branch_zone__id', lookup_expr='in')
    state = NumberInFilter(field_name='state__id', lookup_expr='in')
    city = NumberInFilter(field_name='city__id', lookup_expr='in')
    is_active = filters.BooleanFilter()
    product = filters.NumberFilter(field_name='product_services__product__id')

    class Meta:
        model = ClientBranch
        fields = ['client', 'product', 'branch_name', 'email_id', 'mobile_no', 'branch_zone', 'state', 'city', 'is_active']
