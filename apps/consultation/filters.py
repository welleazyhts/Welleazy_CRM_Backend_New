import django_filters
from .models import ConsultationCase


class ConsultationCaseFilter(django_filters.FilterSet):
    
    corporate_name = django_filters.NumberFilter(field_name='corporate_name__id')
    
    case_status = django_filters.NumberFilter(field_name='case_status__id')
    
    application_no = django_filters.CharFilter(field_name='application_no', lookup_expr='icontains')
    
    case_id = django_filters.CharFilter(field_name='case_id', lookup_expr='icontains')
    
    branch_name = django_filters.NumberFilter(field_name='branch_name__id')
    
    case_rec_mode = django_filters.CharFilter(field_name='case_rec_mode')
    
    assigned_executive = django_filters.CharFilter(field_name='assigned_executive', lookup_expr='icontains')
    
    state = django_filters.NumberFilter(field_name='state__id')
    
    city = django_filters.NumberFilter(field_name='city__id')
    
    follow_up_date_from = django_filters.DateFilter(field_name='follow_up_date_time', lookup_expr='gte')
    follow_up_date_to = django_filters.DateFilter(field_name='follow_up_date_time', lookup_expr='lte')
    
    case_receive_date_from = django_filters.DateFilter(field_name='case_rec_date_time', lookup_expr='gte')
    case_receive_date_to = django_filters.DateFilter(field_name='case_rec_date_time', lookup_expr='lte')
    
    mobile_no = django_filters.CharFilter(field_name='customer_mobile', lookup_expr='icontains')
    
    case_owner_name = django_filters.CharFilter(field_name='customer_name', lookup_expr='icontains')
    
    consultation_type = django_filters.NumberFilter(field_name='consultation_type__id')
    payment_status = django_filters.CharFilter(field_name='payment_status')
    customer_type = django_filters.CharFilter(field_name='customer_type')
    
    class Meta:
        model = ConsultationCase
        fields = [
            'corporate_name', 'case_status', 'application_no', 'case_id',
            'branch_name', 'case_rec_mode', 'assigned_executive', 'state', 'city',
            'follow_up_date_from', 'follow_up_date_to',
            'case_receive_date_from', 'case_receive_date_to',
            'mobile_no', 'case_owner_name',
            'consultation_type', 'payment_status', 'customer_type'
        ]
