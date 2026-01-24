from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import (MasterProduct, MasterProductFor, MasterProductSubCategory, ServiceMapping, 
                    State, City, MasterBranch, DoctorQualification, DoctorSpecialization, MasterPermission, MasterSubPermission,
                    MasterTypeOfInsurance, MasterInsuranceCompany, MasterSpeciality,
                    MasterTypeOfProvider, MasterMedicalSurgeryType, MasterMedicalSurgery,
                    MasterPharmacyPartner, MasterMERType, MasterVisitType, MasterGenericTest,
                    MasterSpecialtiesTest, MasterUploadFormat, MasterLoginType,
                    )
from .serializers import (
    MasterProductSerializer, MasterProductForSerializer, MasterProductSubCategorySerializer,
    ServiceMappingSerializer, StateSerializer, CitySerializer, MasterBranchSerializer, DoctorQualificationSerializer,
    DoctorSpecializationSerializer, MasterPermissionSerializer, MasterSubPermissionSerializer,
    MasterTypeOfInsuranceSerializer, MasterInsuranceCompanySerializer,
    MasterSpecialitySerializer, MasterTypeOfProviderSerializer,
    MasterMedicalSurgeryTypeSerializer, MasterMedicalSurgerySerializer,
    MasterPharmacyPartnerSerializer, MasterMERTypeSerializer, MasterVisitTypeSerializer, MasterGenericTestSerializer,
    MasterSpecialtiesTestSerializer, MasterUploadFormatSerializer, MasterLoginTypeSerializer
    )
from .filters import (
    MasterProductFilter,
    CityFilter,
    MasterMedicalSurgeryFilter,
    MasterSubPermissionFilter, 
    MasterInsuranceCompanyFilter,
    MasterPharmacyPartnerFilter
    )

class MasterProductForViewSet(viewsets.ModelViewSet):
    queryset = MasterProductFor.objects.all().order_by('name')
    serializer_class = MasterProductForSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterProductViewSet(viewsets.ModelViewSet):
    queryset = MasterProduct.objects.all().order_by('name')
    serializer_class = MasterProductSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MasterProductFilter
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterProductSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = MasterProductSubCategory.objects.all().order_by('name')
    serializer_class = MasterProductSubCategorySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ServiceMappingViewSet(viewsets.ModelViewSet):
    queryset = ServiceMapping.objects.all().order_by('id')
    serializer_class = ServiceMappingSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product']
    search_fields = ['product__name', 'sub_products__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CityFilter
    search_fields = ['name', 'state__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterBranchViewSet(viewsets.ModelViewSet):
    queryset = MasterBranch.objects.all().order_by('name')
    serializer_class = MasterBranchSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'states__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class DoctorQualificationViewSet(viewsets.ModelViewSet):
    queryset = DoctorQualification.objects.all().order_by('name')
    serializer_class = DoctorQualificationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class DoctorSpecializationViewSet(viewsets.ModelViewSet):
    queryset = DoctorSpecialization.objects.all().order_by('name')
    serializer_class = DoctorSpecializationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterPermissionViewSet(viewsets.ModelViewSet):
    queryset = MasterPermission.objects.all().order_by('name')
    serializer_class = MasterPermissionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterSubPermissionViewSet(viewsets.ModelViewSet):
    queryset = MasterSubPermission.objects.all().order_by('name')
    serializer_class = MasterSubPermissionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MasterSubPermissionFilter
    search_fields = ['name', 'permission__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterTypeOfInsuranceViewSet(viewsets.ModelViewSet):
    queryset = MasterTypeOfInsurance.objects.all().order_by('name')
    serializer_class = MasterTypeOfInsuranceSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterInsuranceCompanyViewSet(viewsets.ModelViewSet):
    queryset = MasterInsuranceCompany.objects.all().order_by('name')
    serializer_class = MasterInsuranceCompanySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MasterInsuranceCompanyFilter
    search_fields = ['name', 'type_of_insurance__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
class MasterSpecialityViewSet(viewsets.ModelViewSet):
    queryset = MasterSpeciality.objects.all().order_by('name')
    serializer_class = MasterSpecialitySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterTypeOfProviderViewSet(viewsets.ModelViewSet):
    queryset = MasterTypeOfProvider.objects.all().order_by('name')
    serializer_class = MasterTypeOfProviderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterMedicalSurgeryTypeViewSet(viewsets.ModelViewSet):
    queryset = MasterMedicalSurgeryType.objects.all().order_by('name')
    serializer_class = MasterMedicalSurgeryTypeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterMedicalSurgeryViewSet(viewsets.ModelViewSet):
    queryset = MasterMedicalSurgery.objects.all().order_by('name')
    serializer_class = MasterMedicalSurgerySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MasterMedicalSurgeryFilter
    search_fields = ['name', 'surgery_type__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterPharmacyPartnerViewSet(viewsets.ModelViewSet):
    queryset = MasterPharmacyPartner.objects.all().order_by('name')
    serializer_class = MasterPharmacyPartnerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MasterPharmacyPartnerFilter
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MasterMERTypeViewSet(viewsets.ModelViewSet):
    queryset = MasterMERType.objects.all().order_by('name')         
    serializer_class = MasterMERTypeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterVisitTypeViewSet(viewsets.ModelViewSet):
    queryset = MasterVisitType.objects.all().order_by('name')
    serializer_class = MasterVisitTypeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterGenericTestViewSet(viewsets.ModelViewSet):
    queryset = MasterGenericTest.objects.all().order_by('name')
    serializer_class = MasterGenericTestSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'visit_type']
    search_fields = ['name', 'visit_type__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterSpecialtiesTestViewSet(viewsets.ModelViewSet):
    queryset = MasterSpecialtiesTest.objects.all().order_by('name')
    serializer_class = MasterSpecialtiesTestSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]   
    filterset_fields = ['is_active', 'visit_type']
    search_fields = ['name', 'visit_type__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterUploadFormatViewSet(viewsets.ModelViewSet):
    queryset = MasterUploadFormat.objects.all().order_by('name')
    serializer_class = MasterUploadFormatSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MasterLoginTypeViewSet(viewsets.ModelViewSet):
    queryset = MasterLoginType.objects.all().order_by('name')
    serializer_class = MasterLoginTypeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
