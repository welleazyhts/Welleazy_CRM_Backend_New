from django_filters import rest_framework as filters
from .models import MasterSubPermission, MasterInsuranceCompany, MasterPharmacyPartner
from apps.core.filters import NumberInFilter

class MasterSubPermissionFilter(filters.FilterSet):
    permission = NumberInFilter(field_name='permission__id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = MasterSubPermission
        fields = ['permission', 'is_active']

class MasterInsuranceCompanyFilter(filters.FilterSet):
    type_of_insurance = NumberInFilter(field_name='type_of_insurance__id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = MasterInsuranceCompany
        fields = ['type_of_insurance', 'is_active']

class MasterPharmacyPartnerFilter(filters.FilterSet):
    id = NumberInFilter(field_name='id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = MasterPharmacyPartner
        fields = ['id', 'is_active']
