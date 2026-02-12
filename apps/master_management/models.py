from django.db import models
from apps.core.models import BaseModel

class MasterProductFor(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MasterProduct(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    product_for = models.ManyToManyField(MasterProductFor, related_name='products')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MasterProductSubCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    hni_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ServiceMapping(BaseModel):
    product = models.ForeignKey(MasterProduct, on_delete=models.CASCADE, related_name='service_mappings')
    sub_products = models.ManyToManyField(MasterProductSubCategory, related_name='service_mappings')

    def __str__(self):
        sub_products_names = ", ".join([sp.name for sp in self.sub_products.all()])
        return f"{self.product.name} - [{sub_products_names}]"

class State(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class City(BaseModel):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['name', 'state']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class MasterBranch(BaseModel):
    name = models.CharField(max_length=255)
    states = models.ManyToManyField(State, related_name='branches')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        states_names = ", ".join([state.name for state in self.states.all()])
        return f"{self.name} - [{states_names}]"


class DoctorQualification(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 


class DoctorSpecialization(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='doctor_specializations/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MasterPermission(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 


class MasterSubPermission(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    permission = models.ForeignKey(MasterPermission, on_delete=models.CASCADE, related_name='sub_permissions')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 

class MasterTypeOfInsurance(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 

class MasterInsuranceCompany(BaseModel):
    type_of_insurance = models.ForeignKey(MasterTypeOfInsurance, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type_of_insurance.name} - {self.name}" 

class MasterSpeciality(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MasterTypeOfProvider(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 

class MasterMedicalSurgeryType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MasterMedicalSurgery(BaseModel):
    surgery_type = models.ForeignKey(MasterMedicalSurgeryType, on_delete=models.CASCADE, related_name='surgeries')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.surgery_type.name} - {self.name}" 

class MasterPharmacyPartner(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    partner_site = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pharmacy_partners/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 

class MasterMERType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

class MasterVisitType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MasterGenericTest(BaseModel):
    visit_type = models.ForeignKey('MasterVisitType', on_delete=models.CASCADE, related_name='generic_tests', null=True, blank=True)
    name = models.CharField(max_length=255)
    test_code = models.CharField(max_length=100)
    normal_test_price = models.DecimalField(max_digits=10, decimal_places=2)
    hni_test_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 


class MasterSpecialtiesTest(BaseModel):
    visit_type = models.ForeignKey('MasterVisitType', on_delete=models.CASCADE, related_name='specialties_tests', null=True, blank=True)
    name = models.CharField(max_length=255)
    test_code = models.CharField(max_length=100)
    normal_test_price = models.DecimalField(max_digits=10, decimal_places=2)
    hni_test_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MasterUploadFormat(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    upload_format = models.FileField(upload_to='media/upload_formats/')
    
    def __str__(self):
        return self.name 

class MasterLoginType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MasterRelationship(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MasterLanguage(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 
    

class GymVendors(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 
    
class CaseStatus(BaseModel):
    name = models.CharField(max_length=25 , unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
