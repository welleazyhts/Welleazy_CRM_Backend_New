from django_filters import rest_framework as filters
from .models import SubClient
from apps.core.filters import NumberInFilter, CharInFilter

class SubClientFilter(filters.FilterSet):
    client = NumberInFilter(field_name='client__id', lookup_expr='in')
    name = filters.CharFilter(lookup_expr='icontains')
    email_id = filters.CharFilter(lookup_expr='icontains')
    mobile_no = filters.CharFilter(lookup_expr='icontains')
    corporate_type = NumberInFilter(field_name='corporate_type__id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = SubClient
        fields = ['client', 'name', 'email_id', 'mobile_no', 'corporate_type', 'is_active']
