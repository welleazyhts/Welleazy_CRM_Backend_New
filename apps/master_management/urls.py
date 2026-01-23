from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (MasterProductViewSet, MasterProductSubCategoryViewSet, 
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
router.register(r'master-products', MasterProductViewSet)
router.register(r'master-product-sub-categories', MasterProductSubCategoryViewSet)
router.register(r'service-mappings', ServiceMappingViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
router.register(r'master-branches', MasterBranchViewSet)
router.register(r'doctor-qualifications', DoctorQualificationViewSet)
router.register(r'doctor-specializations', DoctorSpecializationViewSet)
router.register(r'master-permissions', MasterPermissionViewSet)
router.register(r'master-sub-permissions', MasterSubPermissionViewSet)
router.register(r'master-type-of-insurances', MasterTypeOfInsuranceViewSet)
router.register(r'master-insurance-companies', MasterInsuranceCompanyViewSet)
router.register(r'master-specialities', MasterSpecialityViewSet)
router.register(r'master-type-of-providers', MasterTypeOfProviderViewSet)
router.register(r'master-medical-surgery-types', MasterMedicalSurgeryTypeViewSet)
router.register(r'master-medical-surgeries', MasterMedicalSurgeryViewSet)
router.register(r'master-pharmacy-partners', MasterPharmacyPartnerViewSet)
router.register(r'master-mer-types', MasterMERTypeViewSet)
router.register(r'master-visit-types', MasterVisitTypeViewSet)
router.register(r'master-generic-tests', MasterGenericTestViewSet)
router.register(r'master-specialties-tests', MasterSpecialtiesTestViewSet)
router.register(r'master-upload-formats', MasterUploadFormatViewSet)
router.register(r'login-types', MasterLoginTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
