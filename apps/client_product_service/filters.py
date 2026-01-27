from django_filters import rest_framework as filters
from .models import ClientProductService
from apps.core.filters import NumberInFilter

class ClientProductServiceFilter(filters.FilterSet):
    login_type = NumberInFilter(field_name='login_type__id', lookup_expr='in')
    client = NumberInFilter(field_name='client__id', lookup_expr='in')
    branch = NumberInFilter(field_name='branch__id', lookup_expr='in')
    product = NumberInFilter(field_name='product__id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = ClientProductService
        fields = ['login_type', 'client', 'branch', 'product', 'is_active']
