from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()


router.register('empanel-for', EmpanelForViewSet)
router.register('doctor-types', DoctorTypeViewSet)
router.register('meet-locations', MeetLocationViewSet)
router.register('document-types', DocumentTypeViewSet)


urlpatterns = router.urls