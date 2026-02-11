from django.urls import path
from .views import (
    SecondOpinionDropdownsAPI,
    SecondOpinionCaseCreateAPI,
    SecondOpinionCaseBulkUploadAPI,
    SecondOpinionCaseListAPI,
    SecondOpinionCaseExportAPI,
    SecondOpinionAssignDoctorAPI,
    SecondOpinionCaseDetailAPI,
    SecondOpinionCaseUpdateAPI,
    SecondOpinionCaseDeleteAPI,
    ClosedSecondOpinionCaseListAPI,
    ClosedSecondOpinionCaseExportAPI
)

urlpatterns = [
    path("dropdowns/", SecondOpinionDropdownsAPI.as_view()),
    path("case/add/", SecondOpinionCaseCreateAPI.as_view()),
    path("case/export/", SecondOpinionCaseExportAPI.as_view()),
    path("case/assign-doctor/", SecondOpinionAssignDoctorAPI.as_view()),
    path("case/bulk-upload/", SecondOpinionCaseBulkUploadAPI.as_view()),
    path("case/list/", SecondOpinionCaseListAPI.as_view()),
    path("case/<int:pk>/", SecondOpinionCaseDetailAPI.as_view()),
    path("case/<int:pk>/update/", SecondOpinionCaseUpdateAPI.as_view()),
    path("case/<int:pk>/delete/", SecondOpinionCaseDeleteAPI.as_view()),
    path("closed-case/list/", ClosedSecondOpinionCaseListAPI.as_view()),
    path("closed-case/export/", ClosedSecondOpinionCaseExportAPI.as_view()),
]
