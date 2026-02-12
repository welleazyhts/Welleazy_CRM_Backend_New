from rest_framework import serializers
from .models import (MasterProduct, MasterProductFor, MasterProductSubCategory, ServiceMapping, 
                     State, City, MasterBranch, DoctorQualification, DoctorSpecialization, MasterPermission, MasterSubPermission,
                    MasterTypeOfInsurance, MasterInsuranceCompany, MasterSpeciality,
                    MasterTypeOfProvider, MasterMedicalSurgeryType, MasterMedicalSurgery,
                    MasterPharmacyPartner, MasterMERType, MasterVisitType, MasterGenericTest,
                    MasterSpecialtiesTest, MasterUploadFormat, MasterLoginType, MasterRelationship , MasterLanguage , GymVendors , CaseStatus)

class MasterProductForSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterProductFor
        fields = '__all__'

class MasterProductSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    product_for_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MasterProduct
        fields = '__all__'
    
    def get_product_for_details(self, obj):
        return [
            {'id': pf.id, 'name': pf.name} 
            for pf in obj.product_for.all()
        ]

class MasterProductSubCategorySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterProductSubCategory
        fields = '__all__'

class MasterLoginTypeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterLoginType
        fields = '__all__'

class ServiceMappingSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    sub_products_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServiceMapping
        fields = '__all__'
    
    def get_sub_products_details(self, obj):
        return [
            {'id': sp.id, 'name': sp.name} 
            for sp in obj.sub_products.all()
        ]

class StateSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)

    class Meta:
        model = City
        fields = '__all__'

class MasterBranchSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    states_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MasterBranch
        fields = '__all__'
    
    def get_states_details(self, obj):
        return [
            {'id': state.id, 'name': state.name} 
            for state in obj.states.all()
        ]

class DoctorQualificationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = DoctorQualification
        fields = '__all__'

class DoctorSpecializationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = DoctorSpecialization
        fields = '__all__'

class MasterPermissionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterPermission
        fields = '__all__'

class MasterSubPermissionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    permission_name = serializers.CharField(source='permission.name', read_only=True)

    class Meta:
        model = MasterSubPermission
        fields = '__all__'

class MasterTypeOfInsuranceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterTypeOfInsurance
        fields = '__all__'

class MasterInsuranceCompanySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    type_of_insurance_name = serializers.CharField(source='type_of_insurance.name', read_only=True)

    class Meta:
        model = MasterInsuranceCompany
        fields = '__all__'

class MasterSpecialitySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterSpeciality
        fields = '__all__'

class MasterTypeOfProviderSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterTypeOfProvider
        fields = '__all__'

class MasterMedicalSurgeryTypeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterMedicalSurgeryType
        fields = '__all__'

class MasterMedicalSurgerySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    surgery_type_name = serializers.CharField(source='surgery_type.name', read_only=True)

    class Meta:
        model = MasterMedicalSurgery
        fields = '__all__'

class MasterPharmacyPartnerSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterPharmacyPartner
        fields = '__all__'

class MasterMERTypeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterMERType
        fields = '__all__'

class MasterVisitTypeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterVisitType
        fields = '__all__'

class MasterGenericTestSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    visit_type_name = serializers.CharField(source='visit_type.name', read_only=True)

    class Meta:
        model = MasterGenericTest
        fields = '__all__'

class MasterSpecialtiesTestSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    visit_type_name = serializers.CharField(source='visit_type.name', read_only=True)

    class Meta:
        model = MasterSpecialtiesTest
        fields = '__all__'

class MasterUploadFormatSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterUploadFormat
        fields = '__all__'

class MasterRelationshipSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterRelationship
        fields = '__all__'



class MasterLanguageSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = MasterLanguage
        fields = '__all__'


class GymVendorSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = GymVendors
        fields = '__all__'

class CaseStatusSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = CaseStatus
        fields = '__all__'