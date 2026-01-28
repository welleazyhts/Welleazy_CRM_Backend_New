from django_filters import rest_framework as filters
from .models import MasterProduct, City, MasterMedicalSurgery, MasterSubPermission, MasterInsuranceCompany, MasterPharmacyPartner
from apps.core.filters import NumberInFilter

class MasterProductFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='id')
    product_for = NumberInFilter(field_name='product_for__id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = MasterProduct
        fields = ['product', 'product_for', 'is_active', 'name']

class CityFilter(filters.FilterSet):
    state = NumberInFilter(field_name='state__id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = City
        fields = ['state', 'is_active', 'name']

class MasterMedicalSurgeryFilter(filters.FilterSet):
    surgery_type = filters.NumberFilter(field_name='surgery_type_id')
    surgery = filters.NumberFilter(field_name='id')
    is_active = filters.BooleanFilter()

    class Meta:
        model = MasterMedicalSurgery
        fields = ['surgery_type', 'surgery', 'is_active', 'name']

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
    pharmacy_partner = NumberInFilter(field_name='id', lookup_expr='in')
    is_active = filters.BooleanFilter()

    class Meta:
        model = MasterPharmacyPartner
        fields = ['pharmacy_partner', 'is_active']
