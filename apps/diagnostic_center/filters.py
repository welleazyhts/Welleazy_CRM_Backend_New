import django_filters
from .models import DiagnosticCenter

import django_filters
from .models import DiagnosticCenter

class DiagnosticCenterFilter(django_filters.FilterSet):
    grade = django_filters.CharFilter(field_name="grade", lookup_expr="iexact")

    # Boolean coming from UI: true / false
    home_collection = django_filters.BooleanFilter(
        field_name="diagnosticservices__home_collection"
    )

    # Boolean coming from UI: true / false
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = DiagnosticCenter
        fields = ["grade", "home_collection", "is_active"]
