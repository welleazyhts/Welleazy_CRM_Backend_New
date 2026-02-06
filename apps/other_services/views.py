
from django.shortcuts import render

# Create your views here.
import csv
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CareProgram , EyeDentalTreatment , MedicalCamp , CampCase
from apps.test_individual.models import IndividualTest as Test
from .serializers import CareProgramSerializer , EyeDentalTreatmentSerializer , MedicalCampSerializer , CampCaseSerializer
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from rest_framework.response import Response as response

from rest_framework import status


class CareProgramViewSet(ModelViewSet):
    queryset = CareProgram.objects.all().order_by('-id')
    serializer_class = CareProgramSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes=[IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']          # filter by active/inactive
    search_fields = ['care_program_name'] 


    @action(detail=False, methods=['get'], url_path='export-csv')
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="care_programs.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'ID',
            'Care Program Name',
            'Normal Price',
            'Care Program Details',
            'Is Active',
            'Created At'
        ])

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.care_program_name,
                obj.normal_price,
                obj.care_program_details,
                obj.is_active,
                obj.created_at
            ])

        return response
    

    @action(detail=False, methods=['get'], url_path='export-excel')
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        wb = Workbook()
        ws = wb.active
        ws.title = "Care Programs"

    # Header row
        headers = [
            "ID",
            "Care Program Name",
            "Normal Price",
            "Care Program Details",
            "Is Active",
            "Created At"
        ]
        ws.append(headers)

    # Data rows
        for obj in queryset:
            ws.append([
                obj.id,
                obj.care_program_name,
                obj.normal_price,
                obj.care_program_details,
                obj.is_active,
                obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

    # Auto-adjust column width
        for col_num, column_title in enumerate(headers, 1):
            ws.column_dimensions[get_column_letter(col_num)].width = 22

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=care_programs.xlsx'

        wb.save(response)
        return response


# EYE & DENTAL TREATMENTS VIEWSET-----


class EyeDentalTreatmentViewSet(ModelViewSet):
    queryset = EyeDentalTreatment.objects.all().order_by("-id")
    serializer_class = EyeDentalTreatmentSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        treatment_type = self.request.query_params.get("type")
        treatment_name = self.request.query_params.get("treatment_name")
        # is_active = self.request.query_params.get("is_active")

        if treatment_type:
            qs = qs.filter(treatment_type__iexact=treatment_type)

        if treatment_name:
            qs = qs.filter(treatment_name__icontains=treatment_name)

        # if is_active is not None:
        #     if is_active.lower() in ["true", "1", "yes"]:
        #         qs = qs.filter(is_active=True)
        #     elif is_active.lower() in ["false", "0", "no"]:
        #         qs = qs.filter(is_active=False)

        return qs
    


# MEDICAL CAMP VIEWSET-----


class MedicalCampViewSet(ModelViewSet):
    queryset = MedicalCamp.objects.all().order_by("-id")
    serializer_class = MedicalCampSerializer
    permission_classes = [IsAdminUser]
    queryset = MedicalCamp.objects.select_related(
        "main_client", "sub_client", "package", "tests", "camp_state", "camp_city", "network_provider"
    )

    
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):

        serializer.save(updated_by=self.request.user)
        instance = self.get_object()

        # Get the new value user is sending (or keep old if not provided)
        new_request_from = self.request.data.get("camp_request_from", instance.camp_request_from)

        camp = serializer.save()

        # ✅ If changed to "Main Client", clear sub_client
        if new_request_from == "Main Client":
            if camp.sub_client is not None:
                camp.sub_client = None
                camp.save(update_fields=["sub_client"])

    # FILTERS-----

    def apply_filters(self, qs, request):
        camp_request_from = request.query_params.get("camp_request_from")
        client_name = request.query_params.get("client_name")
        sub_client = request.query_params.get("sub_client")
        camp_status = request.query_params.get("camp_status")

        if camp_request_from:
            qs = qs.filter(camp_request_from=camp_request_from)

        if client_name:
            qs = qs.filter(main_client__corporate_name__icontains=client_name)

        if sub_client:
            qs = qs.filter(sub_client_id=sub_client)

        if camp_status:
            qs = qs.filter(camp_status=camp_status)

        return qs
    
    # CAMP LIST---
    @action(detail=False, methods=["get"], url_path="camp-list")
    def camp_list(self, request):
        qs = MedicalCamp.objects.exclude(camp_status="Completed")

        camp_request_from = request.query_params.get("camp_request_from")
        main_client = request.query_params.get("main_client")  
        sub_client = request.query_params.get("sub_client")   
        camp_status = request.query_params.get("camp_status") 

        if camp_request_from:
            values = [v.strip() for v in camp_request_from.split(",") if v.strip()]
            qs = qs.filter(camp_request_from__in=values)

        if main_client:
            ids = [i.strip() for i in main_client.split(",") if i.strip()]
            qs = qs.filter(main_client_id__in=ids)

        if sub_client:
            ids = [i.strip() for i in sub_client.split(",") if i.strip()]
            qs = qs.filter(sub_client_id__in=ids)

        # ✅ Multiple statuses: camp_status=Fresh Case,On Going
        if camp_status:
            statuses = [s.strip() for s in camp_status.split(",") if s.strip()]
            qs = qs.filter(camp_status__in=statuses)

        serializer = MedicalCampSerializer(qs, many=True)
        return response(serializer.data)
    

    # CLOSED/CAMP COMPLETED LIST---
    @action(detail=False, methods=["get"], url_path="closed-list")
    def closed_list(self, request):
        qs = MedicalCamp.objects.filter(camp_status="Completed")

        camp_request_from = request.query_params.get("camp_request_from")
        main_client = request.query_params.get("main_client")
        sub_client = request.query_params.get("sub_client")
        camp_status = request.query_params.get("camp_status")

        if camp_request_from:
            values = [v.strip() for v in camp_request_from.split(",") if v.strip()]
            qs = qs.filter(camp_request_from__in=values)

        if main_client:
            ids = [i.strip() for i in main_client.split(",") if i.strip()]
            qs = qs.filter(main_client_id__in=ids)

        if sub_client:
            ids = [i.strip() for i in sub_client.split(",") if i.strip()]
            qs = qs.filter(sub_client_id__in=ids)

        if camp_status:
            statuses = [s.strip() for s in camp_status.split(",") if s.strip()]
            qs = qs.filter(camp_status__in=statuses)

        serializer = MedicalCampSerializer(qs, many=True)
        return response(serializer.data)
        

# CASE VIEWSET-----

class CampCaseViewSet(ModelViewSet):
    queryset = CampCase.objects.select_related(
        "camp",
        "camp__main_client",
        
    )
    serializer_class = CampCaseSerializer
    permission_classes = [IsAdminUser]


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


    # CASE LIST WITH FILTERS-----
    def get_queryset(self):
        qs = super().get_queryset()

        # Query params
        camp_id = self.request.query_params.get("camp_id")        # MedicalCamp ID
        client_name = self.request.query_params.get("client_name")  # text

        # Filter by camp (FK id)
        if camp_id:
            ids = [i.strip() for i in camp_id.split(",") if i.strip()]
            qs = qs.filter(camp_id__in=ids)
        # Filter by client name (from MedicalCamp -> Client)
        if client_name:
            names = [n.strip() for n in client_name.split(",") if n.strip()]
            qs = qs.filter(camp__main_client__corporate_name__in=names)

        return qs