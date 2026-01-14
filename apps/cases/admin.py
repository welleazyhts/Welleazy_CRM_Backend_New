from django.contrib import admin
from .models import Case, CaseServiceDetails, CaseFinancialDetails, CaseAdditionalDetails

admin.site.register(Case)
admin.site.register(CaseServiceDetails)
admin.site.register(CaseFinancialDetails)
admin.site.register(CaseAdditionalDetails)
