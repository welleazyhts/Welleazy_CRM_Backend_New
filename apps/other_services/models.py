from django.conf import settings
from django.db import models
from apps.client.models import Client
from apps.sub_client.models import SubClient
from apps.test_package.models import TestPackage
from apps.test_individual.models import IndividualTest as Test
from apps.core.models import BaseModel
from django.utils import timezone
from apps.master_management.models import State, City , CaseStatus , MasterProduct , MasterProductSubCategory , MasterRelationship
from apps.core.choices import GENDER_CHOICES
from apps.service_provider.models import ServiceProvider
from apps.doctor.models import Doctor
from apps.client_branch.models import ClientBranch
from apps.client_customer.models import ClientCustomer , ClientCustomerDependent



class CareProgram(BaseModel):
    care_program_name = models.CharField(max_length=255)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    care_program_details = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='care_programs/', null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.care_program_name


# EYE & DENTAL TREATMENTS CREATION-----

class EyeDentalTreatment(BaseModel):
    TREATMENT_TYPE_CHOICES = (
        ("Eye", "Eye"),
        ("Dental", "Dental"),
    )

    treatment_type = models.CharField(
        max_length=10, choices=TREATMENT_TYPE_CHOICES
    )
    treatment_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="treatments/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_treatment_type_display()} - {self.treatment_name}"


# ADD CAMP MODEL----


class MedicalCamp(BaseModel):
    CAMP_STATUS_CHOICES = (
        ("Fresh Case", "Fresh Case"),
        ("Future Date", "Future Date"),
        ("On Going", "On Going"),
        ("Partially Done", "Partially Done"),
        ("Completed", "Completed"),
    )

    REQUEST_FROM_CHOICES = (
        ("Main Client", "Main Client"),
        ("Sub Client", "Sub Client"),
    )

    INVOICE_BELONG_CHOICES = (
        ("WELLEAZY_LAB", "Welleazy Lab"),
        ("WELLEAZY_HEALTHTECH", "Welleazyhealthtech"),
    )

    camp_id = models.CharField(max_length=30, unique=True, editable=False)

    camp_request_from = models.CharField(max_length=15, choices=REQUEST_FROM_CHOICES)

    main_client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="medical_camps"
    )
    sub_client = models.ForeignKey(
        SubClient, on_delete=models.SET_NULL, null=True, blank=True
    )

    package = models.ForeignKey(
        TestPackage, on_delete=models.PROTECT
    )

    # Tests under that package (snapshot for this camp)
    tests = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True, null=True)

    camp_datetime = models.DateTimeField()
    camp_location = models.CharField(max_length=255)
    camp_address = models.TextField()

    camp_state = models.ForeignKey(State, on_delete=models.PROTECT)
    camp_city = models.ForeignKey(City, on_delete=models.PROTECT)

    expected_medical_count = models.PositiveIntegerField(default=0)
    completed_medical_count = models.PositiveIntegerField(default=0)

    camp_status = models.CharField(max_length=20, choices=CAMP_STATUS_CHOICES, default="FRESH")

    client_spoc_name = models.CharField(max_length=255, blank=True)
    client_spoc_mobile = models.CharField(max_length=20, blank=True)
    client_spoc_email = models.EmailField(blank=True)

    network_spoc_name = models.CharField(max_length=255, blank=True)
    network_spoc_mobile = models.CharField(max_length=20, blank=True)
    network_spoc_email = models.EmailField(blank=True)

    client_invoice_belong_to = models.CharField(
        max_length=30,
        choices=INVOICE_BELONG_CHOICES
    )

    client_cost_per_case = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_client_billable_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    network_cost_per_case = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    network_payable_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    network_provider = models.ForeignKey(ServiceProvider
        , on_delete=models.PROTECT, null=True, blank=True
    )

    medical_hard_copy_required = models.BooleanField(default=False)
    special_requirement = models.TextField(blank=True)


    def save(self, *args, **kwargs):
        if not self.camp_id:
            last_id = MedicalCamp.objects.order_by("id").last()
            if last_id:
                num = last_id.id + 1
            else:
                num = 1
            self.camp_id = f"CAMP{num:04d}"  # CAMP00001

        # If completed, keep completed_medical_count, else reset or keep as is
        if self.camp_status != "Completed":
            self.completed_medical_count = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.camp_id


# CASE MODEL-----




class CampCase(BaseModel):
    case_id = models.CharField(max_length=20, unique=True, editable=False)
    customer_id = models.CharField(max_length=20, unique=True, editable=False)

    camp = models.ForeignKey(MedicalCamp, on_delete=models.PROTECT, related_name="cases")

    customer_name = models.CharField(max_length=255)
    customer_mobile = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)

    customer_gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    case_status = models.ForeignKey(CaseStatus, on_delete=models.PROTECT)

    document = models.FileField(upload_to="case_documents/", blank=True, null=True)

   

    def save(self, *args, **kwargs):
        # Auto-generate case_id: WXC00001
        if not self.case_id:
            last = CampCase.objects.order_by("id").last()
            num = last.id + 1 if last else 1
            self.case_id = f"WXC{num:05d}"

        # Auto-generate customer_id: CNR01
        if not self.customer_id:
            last = CampCase.objects.order_by("id").last()
            num = last.id + 1 if last else 1
            self.customer_id = f"CNR{num:02d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.case_id


# COMPREHENSIVE HEALTH PLANS------


class CHP(BaseModel):
    CATEGORY_CHOICES = (
        ("NA", "NA"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Half Yearly", "Half Yearly"),
        ("Annually", "Annually"),
    )

    FREQUENCY_CHOICES = (
        ("NA", "NA"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Half Yearly", "Half Yearly"),
        ("Annually", "Annually"),
    )

    package = models.ForeignKey(TestPackage, on_delete=models.PROTECT)

    # These two are choices now
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="NA")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="NA")

    product = models.ForeignKey(MasterProduct, on_delete=models.PROTECT)  
    service = models.ForeignKey(MasterProductSubCategory, on_delete=models.PROTECT) 

    limitation = models.CharField(max_length=255, blank=True)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    corporate_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.package} - {self.product}"



# OHC MASTER TABLE-----


class TypeOfOHC(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

# OHC MAIN TABLE------


class OHC(BaseModel):
    type_of_ohc = models.ForeignKey(TypeOfOHC, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)

    corporate_requirements = models.TextField(blank=True)
    crm_name = models.CharField(max_length=255, blank=True)

    corporate_address = models.TextField(blank=True)

    spoc_name = models.CharField(max_length=255, blank=True)
    spoc_email = models.EmailField(blank=True)
    spoc_mobile = models.CharField(max_length=20, blank=True)

    # Date + Time
    service_start_date = models.DateTimeField(null=True, blank=True)
    agreement_date = models.DateTimeField(null=True, blank=True)
    relationship_end_date = models.DateTimeField(null=True, blank=True)

    agreement_upload = models.FileField(upload_to="ohc_agreements/", null=True, blank=True)

    client_bill_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    service_provider_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # These two:
    doctor_qualifications = models.CharField(max_length=255, blank=True)
    doctor_certificate_link = models.URLField(blank=True)

    remarks = models.TextField(blank=True)

   

    def __str__(self):
        return f"{self.client} - {self.type_of_ohc}"


# EYE PROCEDURE MODULE------


class EyeTreatmentCase(BaseModel):

    case_id = models.CharField(max_length=20, unique=True, editable=False)

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    branch = models.ForeignKey(ClientBranch, on_delete=models.PROTECT)

    employee = models.ForeignKey(
        ClientCustomer,
        on_delete=models.PROTECT,
        related_name='eye_treatment_cases'
    )

    case_for = models.ForeignKey(
        MasterRelationship,
        on_delete=models.PROTECT
    )

    # Store dependent only when not SELF
    relationship_person = models.ForeignKey(
        ClientCustomerDependent,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='eye_treatment_cases'
    )

    # Single, stored name (auto-prefilled but editable)
    customer_name = models.CharField(max_length=255)

    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField()

    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    address = models.TextField(blank=True, null=True)

    eye_treatment = models.ForeignKey(
        EyeDentalTreatment,
        on_delete=models.PROTECT
    )

    case_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT
    )

    comment = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

   

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.case_id:
            self.case_id = f"WZCP{self.pk:06d}"
            super().save(update_fields=['case_id'])


# DENTAL PROCEDURE MODULE------



class DentalTreatmentCase(BaseModel):
    case_id = models.CharField(max_length=20, unique=True, editable=False)

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    branch = models.ForeignKey(ClientBranch, on_delete=models.PROTECT)

    employee = models.ForeignKey(
        ClientCustomer,
        on_delete=models.PROTECT,
        related_name='dental_treatment_cases'
    )

    case_for = models.ForeignKey(MasterRelationship, on_delete=models.PROTECT)

    # Only when not SELF
    relationship_person = models.ForeignKey(
        ClientCustomerDependent,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='dental_treatment_cases'
    )

    customer_name = models.CharField(max_length=255)

    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField()

    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    address = models.TextField(blank=True, null=True)

    # Same master table as Eye, but filtered by type in serializer/view
    dental_treatment = models.ForeignKey(EyeDentalTreatment, on_delete=models.PROTECT)

    case_status = models.ForeignKey(CaseStatus, on_delete=models.PROTECT)

    comment = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


 

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.case_id:
            self.case_id = f"WZCP{self.pk:06d}"
            super().save(update_fields=['case_id'])

    def __str__(self):
        return self.case_id
