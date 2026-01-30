from django.urls import path
from .views import *

urlpatterns = [
    path("case-received-modes/", CaseReceivedModeAPI.as_view()),
    path("case-types/", CaseTypeAPI.as_view()),
    path("payment-types/", PaymentTypeAPI.as_view()),
    path("case-fors/", CaseForAPI.as_view()),
    path("preferred-visit-types/", PreferredVisitTypeAPI.as_view()),
    path("case-status/", CaseStatusAPI.as_view()),
    path("customer-types/", CustomerTypeAPI.as_view()),
    path("service-offered/", ServiceOfferedAPI.as_view()),
    path("genders/", GenderAPI.as_view()),
    path("medical-tests/", MedicalTestAPI.as_view()),
    path("generic-tests/", GenericTestAPI.as_view()),
    path("customer-profiles/", CustomerProfileAPI.as_view()),
    path("dhoc-payment-options/", DhocPaymentOptionAPI.as_view()),
]
