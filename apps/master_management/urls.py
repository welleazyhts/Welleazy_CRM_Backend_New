from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (MasterProductViewSet, MasterProductForViewSet, MasterProductSubCategoryViewSet, 
                    MasterBranchViewSet, ServiceMappingViewSet, StateViewSet, CityViewSet,
                    DoctorQualificationViewSet, DoctorSpecializationViewSet, MasterPermissionViewSet,
                    MasterSubPermissionViewSet, MasterTypeOfInsuranceViewSet,
                    MasterInsuranceCompanyViewSet, MasterSpecialityViewSet,
                    MasterTypeOfProviderViewSet, MasterMedicalSurgeryTypeViewSet,
                    MasterMedicalSurgeryViewSet, MasterPharmacyPartnerViewSet,
                    MasterMERTypeViewSet, MasterVisitTypeViewSet, MasterGenericTestViewSet,
                    MasterSpecialtiesTestViewSet, MasterUploadFormatViewSet,
                    MasterLoginTypeViewSet)

router = DefaultRouter()
router.register(r'products', MasterProductViewSet)
router.register(r'product-fors', MasterProductForViewSet)
router.register(r'product-sub-categories', MasterProductSubCategoryViewSet)
router.register(r'service-mappings', ServiceMappingViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
router.register(r'branches', MasterBranchViewSet)
router.register(r'doctor-qualifications', DoctorQualificationViewSet)
router.register(r'doctor-specializations', DoctorSpecializationViewSet)
router.register(r'permissions', MasterPermissionViewSet)
router.register(r'sub-permissions', MasterSubPermissionViewSet)
router.register(r'type-of-insurances', MasterTypeOfInsuranceViewSet)
router.register(r'insurance-companies', MasterInsuranceCompanyViewSet)
router.register(r'specialities', MasterSpecialityViewSet)
router.register(r'type-of-providers', MasterTypeOfProviderViewSet)
router.register(r'medical-surgery-types', MasterMedicalSurgeryTypeViewSet)
router.register(r'medical-surgeries', MasterMedicalSurgeryViewSet)
router.register(r'pharmacy-partners', MasterPharmacyPartnerViewSet)
router.register(r'mer-types', MasterMERTypeViewSet)
router.register(r'visit-types', MasterVisitTypeViewSet)
router.register(r'generic-tests', MasterGenericTestViewSet)
router.register(r'specialties-tests', MasterSpecialtiesTestViewSet)
router.register(r'upload-formats', MasterUploadFormatViewSet)
router.register(r'login-types', MasterLoginTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
