from django.db import models
from apps.core.models import BaseModel

# ================= CLIENT & BRANCH =================
from apps.client.models import Client
from apps.client_branch.models import ClientBranch

# ================= PHYSICAL MEDICAL MASTERS =================
from apps.physical_medical_master.models import (
    CaseReceivedMode,
    CaseType,
    PaymentType,
    CaseFor,
    PreferredVisitType,
    CaseStatus,
    CustomerType,
    ServiceOffered,
    Gender,
    MedicalTest,
    CustomerProfile,
    DhocPaymentOption
)

# ================= MASTER MANAGEMENT =================
from apps.master_management.models import (
    State,
    City,
    MasterProduct,
    MasterGenericTest
)


# ====================================================
# 1️⃣ PHYSICAL MEDICAL CASE (MAIN)
# ====================================================
class PhysicalMedicalCase(BaseModel):

    case_id = models.CharField(max_length=20, unique=True, editable=False)

    case_received_mode = models.ForeignKey(CaseReceivedMode, on_delete=models.SET_NULL, null=True)
    case_received_datetime = models.DateTimeField(null=True, blank=True)
    case_status = models.ForeignKey(CaseStatus, on_delete=models.SET_NULL, null=True)
    
    assigned_executive = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )


    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = f"WX{PhysicalMedicalCase.objects.count()+1:05d}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = "physical_medicals_physicalmedicalcase"

    def __str__(self):
        return self.case_id


# ====================================================
# 2️⃣ CLIENT DETAILS
# ====================================================
class PhysicalMedicalClientDetail(BaseModel):

    case = models.OneToOneField(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="client_detail"
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_branch = models.ForeignKey(ClientBranch, on_delete=models.CASCADE)

    customer_type = models.ForeignKey(CustomerType, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(MasterProduct, on_delete=models.SET_NULL, null=True)
    service_offered = models.ForeignKey(ServiceOffered, on_delete=models.SET_NULL, null=True)

    received_by_name = models.CharField(max_length=255, blank=True)
    received_mobile = models.CharField(max_length=15, blank=True)
    received_email = models.EmailField(blank=True)
    department = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "physical_medicals_physicalmedicalclientdetail"


# ====================================================
# 3️⃣ CUSTOMER DETAILS
# ====================================================
class PhysicalMedicalCustomerDetail(BaseModel):

    case = models.OneToOneField(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="customer_detail"
    )

    customer_id = models.CharField(max_length=20, unique=True, editable=False)
    customer_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15, blank=True)

    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    email_id = models.EmailField(blank=True)

    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    pincode = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    area_locality = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=255, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    geo_location = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            self.customer_id = f"EMP{PhysicalMedicalCustomerDetail.objects.count()+1:08d}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = "physical_medicals_physicalmedicalcustomerdetail"


# ====================================================
# 4️⃣ CASE DETAILS
# ====================================================
class PhysicalMedicalCaseDetail(BaseModel):

    case = models.OneToOneField(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="case_detail"
    )

    medical_test = models.ForeignKey(MedicalTest, on_delete=models.SET_NULL, null=True)
    generic_test = models.ForeignKey(MasterGenericTest, on_delete=models.SET_NULL, null=True)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True)

    application_no = models.CharField(max_length=50)
    case_type = models.ForeignKey(CaseType, on_delete=models.SET_NULL, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True)
    case_for = models.ForeignKey(CaseFor, on_delete=models.SET_NULL, null=True)

    dhoc_payment = models.ForeignKey(DhocPaymentOption, on_delete=models.SET_NULL, null=True)
    customer_pay_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    preferred_visit_type = models.ForeignKey(PreferredVisitType, on_delete=models.SET_NULL, null=True)
    preferred_appointment_datetime = models.DateTimeField(null=True, blank=True)

    company_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "physical_medicals_physicalmedicalcasedetail"


# ====================================================
# 5️⃣ DEPENDENTS (ADD CASE LIST)
# ====================================================
class PhysicalMedicalDependent(BaseModel):

    case = models.ForeignKey(
        PhysicalMedicalCase,
        on_delete=models.CASCADE,
        related_name="dependents"
    )

    case_for = models.ForeignKey(CaseFor, on_delete=models.SET_NULL, null=True)
    dependent_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)

    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()

    address = models.TextField(blank=True)
    medical_test = models.ForeignKey(MedicalTest, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "physical_medicals_physicalmedicaldependent"
