from django.db import models

# Create your models here.

from apps.client.models import Client
from apps.sub_client.models import SubClient
from apps.test_package.models import TestPackage
from apps.test_individual.models import IndividualTest as Test
from apps.core.models import BaseModel
from django.utils import timezone
from apps.master_management.models import State, City , MasterGender , CaseStatus
from apps.service_provider.models import ServiceProvider


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

    customer_gender = models.ForeignKey(MasterGender, on_delete=models.PROTECT)
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
