import django_filters
from .models import MiscellaneousProgramCase

class MiscellaneousProgramCaseFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(lookup_expr='icontains')
    case_id = django_filters.CharFilter(lookup_expr='icontains')
    mobile_no = django_filters.CharFilter(lookup_expr='icontains')
    client = django_filters.NumberFilter(field_name='client__id')
    branch = django_filters.NumberFilter(field_name='branch__id')
    case_status = django_filters.NumberFilter(field_name='case_status__id')
    case_for = django_filters.NumberFilter(field_name='case_for__id')
    state = django_filters.NumberFilter(field_name='state__id')
    city = django_filters.NumberFilter(field_name='city__id')
    updated_by = django_filters.NumberFilter(field_name='updated_by__id')
    
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    
    list_type = django_filters.ChoiceFilter(
        choices=[('open', 'Open'), ('closed', 'Closed')],
        method='filter_by_list_type'
    )

    def filter_by_list_type(self, queryset, name, value):
        if value == 'open':
            return queryset.filter(case_status__name__in=['Fresh Case', 'In Process'])
        elif value == 'closed':
            return queryset.filter(case_status__name__in=['Completed', 'Closed', 'Cancelled', 'Rejected'])
        return queryset

    class Meta:
        model = MiscellaneousProgramCase
        fields = [
            'client', 'branch', 'case_status', 'case_for', 
            'care_program', 'list_type', 'state', 'city', 
            'updated_by'
        ]
