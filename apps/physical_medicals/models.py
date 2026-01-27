from django.db import models
from django.db import models

from apps.master_management.models import (
    MasterProduct,
    State,
    City,
    ServiceMapping, 
    MasterGenericTest
)


class PhysicalMedicalCase(models.Model):
    case_id = models.CharField(max_length=20, unique=True)

    case_entry_datetime = models.DateTimeField()
    case_received_mode = models.CharField(max_length=50)
    case_received_datetime = models.DateTimeField()

    welleazy_branch = models.CharField(max_length=100)
    assigned_executive = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case_id
class PhysicalMedicalClientDetail(models.Model):
    case = models.OneToOneField(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="client_detail"
    )

    client_name = models.CharField(max_length=255)
    branch_zone = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100)

    customer_type = models.CharField(max_length=20)  # Employee / Candidate

    product = models.ForeignKey(
        MasterProduct,
        on_delete=models.PROTECT,
        related_name="physical_medical_clients"
    )
    services_offered = models.ForeignKey(
        ServiceMapping,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="physical_medical_services"
    )

    received_by = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
class PhysicalMedicalCustomerDetail(models.Model):
    case = models.OneToOneField(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="customer_detail"
    )

    customer_id = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=255)

    mobile_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15, blank=True, null=True)

    gender = models.CharField(max_length=10)
    email_id = models.EmailField()

    state = models.ForeignKey(State,on_delete=models.PROTECT,related_name="physical_medical_cases")
    
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="physical_medical_cases"
    )


    address = models.TextField()
    area = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    geo_location = models.CharField(max_length=255, blank=True, null=True)
class PhysicalMedicalCaseDetail(models.Model):
    case = models.OneToOneField(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="case_detail"
    )

    medical_test = models.CharField(max_length=100)
    generic_test = models.ForeignKey(MasterGenericTest,on_delete=models.PROTECT,related_name="physical_medical_cases",
        blank=True,
        null=True
    )

    customer_profile = models.CharField(max_length=50)
    customer_pay_amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    application_no = models.CharField(max_length=50)
    case_type = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    case_for = models.CharField(max_length=50)

    dhoc_payment = models.CharField(
    max_length=10,
    null=True,
    blank=True
)

    preferred_visit_type = models.CharField(
        max_length=50, null=True, blank=True
    )
    company_name = models.CharField(max_length=150, blank=True, null=True)

    preferred_appointment_datetime = models.DateTimeField(
        null=True, blank=True
    )

   

    arrange_appointment = models.BooleanField(default=False)

    case_status = models.CharField(max_length=100)
    follow_up_date = models.DateField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
