import django_filters
from .models import GymPackage

class GymPackageFilter(django_filters.FilterSet):

    # Exact match for SKU
    gym_sku = django_filters.CharFilter(
        field_name="gym_sku",
        lookup_expr="iexact"
    )

    # Partial search for package name
    package_name = django_filters.CharFilter(
        field_name="package_name",
        lookup_expr="icontains"
    )

    # Status filter (true / false)
    status = django_filters.BooleanFilter(
        field_name="status"
    )

    class Meta:
        model = GymPackage
        fields = ["gym_sku", "package_name", "status"]
