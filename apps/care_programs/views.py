from django.shortcuts import render

# Create your views here.



from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CareProgramCase
from .serializers import CareProgramCaseSerializer
from apps.client_customer.models import ClientCustomer, ClientCustomerDependent
from apps.master_management.models import MasterRelationship , CaseStatus
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAdminUser



class CareProgramCaseViewSet(ModelViewSet):
    queryset = CareProgramCase.objects.all().order_by('-id')
    serializer_class = CareProgramCaseSerializer
    permission_classes = [IsAdminUser]

    # -----------------------------
    # CUSTOMER NAME DROPDOWN
    # -----------------------------
    @action(detail=False, methods=['get'], url_path='relationship-persons')
    def relationship_persons(self, request):
        employee_id = request.query_params.get('employee_id')
        case_for_id = request.query_params.get('case_for_id')

        relationship = MasterRelationship.objects.get(id=case_for_id)

        # SELF → no dropdown
        if relationship.name.lower() == 'self':
            return Response([])

        dependents = ClientCustomerDependent.objects.filter(
            customer_id=employee_id,
            relationship_id=case_for_id
        )

        return Response([
            {
                "id": d.id,
                "name": d.name
            } for d in dependents
        ])
    


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



# FOR OPEN CASE VIEWSET-------



class OpenCareProgramCaseViewSet(ReadOnlyModelViewSet):
    serializer_class = CareProgramCaseSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = CareProgramCase.objects.all()

        # -------------------------
        # BASE CONDITION: OPEN CASES
        # -------------------------
        open_statuses = CaseStatus.objects.filter(
            name__in=["Fresh Case", "In Process"]
        )
        qs = qs.filter(case_status__in=open_statuses)

        params = self.request.query_params

        # -------------------------
        # MULTI-SELECT FILTERS
        # -------------------------
        def multi_filter(field):
            value = params.get(field)
            if value:
                ids = value.split(',')
                return Q(**{f"{field}__in": ids})
            return Q()

        qs = qs.filter(
            multi_filter('client') &
            multi_filter('case_status') &
            multi_filter('care_program') &
            multi_filter('updated_by_name')&
            multi_filter('state') &
            multi_filter('city') &
            multi_filter('case_for') &
            multi_filter('employee')
        )

        # -------------------------
        # TEXT FILTERS
        # -------------------------
        if params.get('mobile_number'):
            qs = qs.filter(
                mobile_number__icontains=params.get('mobile_number')
            )

        if params.get('case_id'):
            qs = qs.filter(
                case_id__icontains=params.get('case_id')
            )

        # -------------------------
        # DATE RANGE FILTER
        # -------------------------
        start_date = parse_date(params.get('start_date', ''))
        end_date = parse_date(params.get('end_date', ''))

        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)

        return qs.order_by('-id')


# CLOSED CASE LISTING VIEWSET-----


class ClosedCareProgramCaseViewSet(ReadOnlyModelViewSet):
    serializer_class = CareProgramCaseSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = CareProgramCase.objects.all()

        # -------------------------
        # BASE CONDITION: CLOSED
        # -------------------------
        completed_status = CaseStatus.objects.filter(
            name="Completed"
        )
        qs = qs.filter(case_status__in=completed_status)

        params = self.request.query_params

        # -------------------------
        # MULTI-SELECT FILTERS
        # -------------------------
        def multi_filter(field):
            value = params.get(field)
            if value:
                return Q(**{f"{field}__in": value.split(',')})
            return Q()

        qs = qs.filter(
            multi_filter('client') &
            multi_filter('case_status') &
            multi_filter('care_program') &
            multi_filter('updated_by_name')&
            multi_filter('state') &
            multi_filter('city') &
            multi_filter('case_for') &
            multi_filter('employee')
        )

        # -------------------------
        # TEXT FILTERS
        # -------------------------
        if params.get('mobile_number'):
            qs = qs.filter(
                mobile_number__icontains=params.get('mobile_number')
            )

        if params.get('case_id'):
            qs = qs.filter(
                case_id__icontains=params.get('case_id')
            )

        # -------------------------
        # DATE RANGE FILTER
        # -------------------------
        start_date = parse_date(params.get('start_date', ''))
        end_date = parse_date(params.get('end_date', ''))

        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)

        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)

        return qs.order_by('-id')