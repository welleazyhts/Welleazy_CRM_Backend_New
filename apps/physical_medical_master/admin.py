from django.contrib import admin
from .models import *

admin.site.register(CaseReceivedMode)
admin.site.register(CaseType)
admin.site.register(PaymentType)
admin.site.register(CaseFor)
admin.site.register(PreferredVisitType)
admin.site.register(CaseStatus)

admin.site.register(CustomerType)
admin.site.register(ServiceOffered)



admin.site.register(MedicalTest)
admin.site.register(CustomerProfile)
admin.site.register(DhocPaymentOption)
