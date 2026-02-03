from django.shortcuts import render

# Create your views here.
import csv
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CareProgram
from .serializers import CareProgramSerializer
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

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

