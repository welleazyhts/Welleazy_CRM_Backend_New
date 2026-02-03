from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from .models import GymPackage , PackagePriceType
from .serializers import GymPackageSerializer , PackagePriceTypeSerializer
from rest_framework.permissions import IsAdminUser
from .filters import GymPackageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import csv
from django.http import HttpResponse
from rest_framework.decorators import action
from openpyxl import Workbook



# VIEW OF MASTER TABLE----

class PackagePriceViewSet(ModelViewSet):
    queryset = PackagePriceType.objects.all().order_by('name')
    serializer_class = PackagePriceTypeSerializer
    permission_classes = [IsAdminUser] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



# MAIN VIEWSET-----

class GymPackageViewSet(ModelViewSet):
    queryset = GymPackage.objects.all().order_by('-created_at')
    serializer_class = GymPackageSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_class = GymPackageFilter

# CSV EXPORT---

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="gym_packages.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Gym SKU",
            "Package Name",
            "Plan Category",
            "Package Price",
            "Actual Price",
            "Discount %",
            "Discounted Price",
            "City",
            "Status"
        ])

        for pkg in queryset:
            writer.writerow([
                pkg.gym_sku,
                pkg.package_name,
                pkg.plan_category.name,
                pkg.package_price.name,
                pkg.actual_price,
                pkg.discount_percentage,
                pkg.discounted_package_price,
                pkg.city.name,
                "Active" if pkg.status else "Inactive"
            ])

        return response
    
# EXCEL EXPORT----
    @action(detail=False, methods=["get"], url_path="export-excel")
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Gym Packages"

        headers = [
            "Gym SKU",
            "Package Name",
            "Plan Category",
            "Package Price",
            "Actual Price",
            "Discount %",
            "Discounted Price",
            "City",
            "Status"
        ]
        sheet.append(headers)

        for pkg in queryset:
            sheet.append([
                pkg.gym_sku,
                pkg.package_name,
                pkg.plan_category.name,
                pkg.package_price.name,
                float(pkg.actual_price),
                pkg.discount_percentage,
                float(pkg.discounted_package_price),
                pkg.city.name,
                "Active" if pkg.status else "Inactive"
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="gym_packages.xlsx"'

        workbook.save(response)
        return response