from django.urls import path
from .views import (
    PhysicalMedicalAddCaseAPI,
    PhysicalMedicalGetCaseAPI
)

urlpatterns = [
    path("add-case/", PhysicalMedicalAddCaseAPI.as_view()),
    path("get-case/<str:case_id>/", PhysicalMedicalGetCaseAPI.as_view()),
]
