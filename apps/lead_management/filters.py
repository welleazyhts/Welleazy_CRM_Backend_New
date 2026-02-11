import django_filters
from .models import Lead


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class LeadFilter(django_filters.FilterSet):
    
    lead_source = NumberInFilter(field_name="lead_source__id", lookup_expr='in')
    lead_status = NumberInFilter(field_name="lead_status__id", lookup_expr='in')
    lead_type = CharInFilter(field_name='lead_type', lookup_expr='in')
    
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone_no = django_filters.CharFilter(lookup_expr='icontains')
    
    state = NumberInFilter(field_name="state__id", lookup_expr='in')
    city = NumberInFilter(field_name="city__id", lookup_expr='in')
    gender = NumberInFilter(field_name="gender__id", lookup_expr='in')
    
    service_type = CharInFilter(field_name='service_type', lookup_expr='in')
    service_category = CharInFilter(field_name='service_category', lookup_expr='in')
    
    renewal_date = django_filters.DateFilter()
    renewal_date_from = django_filters.DateFilter(field_name='renewal_date', lookup_expr='gte')
    renewal_date_to = django_filters.DateFilter(field_name='renewal_date', lookup_expr='lte')
    
    reminder_date = django_filters.DateFilter()
    reminder_date_from = django_filters.DateFilter(field_name='reminder_date', lookup_expr='gte')
    reminder_date_to = django_filters.DateFilter(field_name='reminder_date', lookup_expr='lte')
    
    follow_up_date = django_filters.DateFilter()
    follow_up_date_from = django_filters.DateFilter(field_name='follow_up_date', lookup_expr='gte')
    follow_up_date_to = django_filters.DateFilter(field_name='follow_up_date', lookup_expr='lte')
    
    receive_email = django_filters.BooleanFilter()
    receive_sms = django_filters.BooleanFilter()
    receive_whatsapp = django_filters.BooleanFilter()
    
    class Meta:
        model = Lead
        fields = [
            'lead_type', 'lead_source', 'lead_status',
            'first_name', 'last_name', 'company_name', 'email', 'phone_no',
            'state', 'city', 'gender',
            'service_type', 'service_category',
            'renewal_date', 'renewal_date_from', 'renewal_date_to',
            'reminder_date', 'reminder_date_from', 'reminder_date_to',
            'follow_up_date', 'follow_up_date_from', 'follow_up_date_to',
            'receive_email', 'receive_sms', 'receive_whatsapp'
        ]
