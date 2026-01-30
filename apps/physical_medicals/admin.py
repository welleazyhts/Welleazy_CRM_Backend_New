from django.contrib import admin
from .models import (
    PhysicalMedicalCase,
    PhysicalMedicalClientDetail,
    PhysicalMedicalCustomerDetail,
    PhysicalMedicalCaseDetail
)

admin.site.register(PhysicalMedicalCase)
admin.site.register(PhysicalMedicalClientDetail)
admin.site.register(PhysicalMedicalCustomerDetail)
admin.site.register(PhysicalMedicalCaseDetail)
