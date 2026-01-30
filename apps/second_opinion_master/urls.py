from django.urls import path
from .views import *

urlpatterns = [
    path('case-types/', SecondOpinionCaseTypeAPI.as_view()),
    path('interpretation-types/', InterpretationTypeAPI.as_view()),
    path("case-received-modes/", CaseReceivedModeAPI.as_view()),
]
