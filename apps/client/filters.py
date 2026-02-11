from django_filters import rest_framework as filters
from .models import Client

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ClientFilter(filters.FilterSet):
    business_type = NumberInFilter(field_name="business_type__id", lookup_expr='in')
    corporate_type = NumberInFilter(field_name="corporate_type__id", lookup_expr='in')
    frequency_of_payment = NumberInFilter(field_name="frequency_of_payment__id", lookup_expr='in')
    client_agreement_from = NumberInFilter(field_name="client_agreement_from__id", lookup_expr='in')

    corporate_code = CharInFilter(field_name='corporate_code', lookup_expr='in')
    corporate_name = CharInFilter(field_name='corporate_name', lookup_expr='in')
    email_id = filters.CharFilter(lookup_expr='icontains')
    mobile_no = filters.CharFilter(lookup_expr='icontains')
    
    is_active = filters.BooleanFilter()

    # Search in product services
    product = filters.NumberFilter(field_name="product_services__product__id")
    product_name = filters.CharFilter(field_name="product_services__product__name", lookup_expr='icontains')
    services_offered = filters.CharFilter(field_name="product_services__services__name", lookup_expr='icontains')

    class Meta:
        model = Client
        fields = [
            'business_type', 'corporate_code', 'corporate_name', 
            'corporate_type', 'email_id', 'mobile_no', 
            'is_active', 'frequency_of_payment', 'client_agreement_from',
            'product', 'product_name', 'services_offered'
        ]
