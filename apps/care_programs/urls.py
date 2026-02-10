from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.care_programs.views import CareProgramCaseViewSet, ClosedCareProgramCaseViewSet, OpenCareProgramCaseViewSet



router = DefaultRouter()
router.register(r'care-program-cases',CareProgramCaseViewSet,basename='care-program-cases')



urlpatterns = [
    path('', include(router.urls)),
    path('open-care-program-cases/',OpenCareProgramCaseViewSet.as_view({'get': 'list'}),name='open-care-program-cases'),
    path('closed-care-program-cases/',ClosedCareProgramCaseViewSet.as_view({'get': 'list'}),name='closed-care-program-cases'),
]
