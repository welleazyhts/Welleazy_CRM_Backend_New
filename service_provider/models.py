from django.db import models

# Create your models here.


from django.db import models
from apps.core.models import BaseModel
from apps.service_provider_master.models import (
    ProviderType,
    PartnershipType,
    SpecialtyType,
    OwnershipType,
    MedicalSpeciality,
    ServiceCategory,
    RadiologyType,
    DiscountService,
    VoucherDiscountType,
    DCUniqueName,
    PaymentTerm,
    Client
)
# from apps.admin_app.modules.clients.models import Client
# from apps.locations.models import City, State


# =====================================================
# SERVICE PROVIDER (MAIN)
# =====================================================
class ServiceProvider(BaseModel):

    # ---------- IDENTIFIERS ----------
    sp_code = models.CharField(max_length=50, unique=True, null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
        default="Yes"
    )

    is_active = models.BooleanField(default=True)

    # ---------- MASTER FKs ----------
    provider_type = models.ForeignKey(MasterTypeOfProvider, on_delete=models.PROTECT)
    partnership_type = models.ForeignKey(PartnershipType, on_delete=models.PROTECT)
    specialty_type = models.ForeignKey(SpecialtyType, on_delete=models.PROTECT)
    ownership_type = models.ForeignKey(OwnershipType, on_delete=models.PROTECT)

    visit_type = models.CharField(
        max_length=20,
        choices=[
            ("Center", "Center"),
            ("Home", "Home"),
            ("Both", "Both"),
        ]
    )

    dc_unique_name = models.ForeignKey(DCUniqueName, on_delete=models.PROTECT)
    payment_term = models.ForeignKey(
        PaymentTerm, on_delete=models.SET_NULL, null=True, blank=True
    )

    # ---------- CORPORATE ----------
    corporate_group = models.CharField(
        max_length=3,
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
        default="No"
    )

    client_company = models.ManyToManyField(Client, blank=True)

    # ---------- BASIC DETAILS ----------
    center_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    landline = models.CharField(max_length=20, null=True, blank=True)
    std_code = models.CharField(max_length=10, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)

    plot_no = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    area = models.CharField(max_length=100)

    city = models.ForeignKey(City, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    pin_code = models.CharField(max_length=10)
    service_pin_code = models.CharField(max_length=10)

    website = models.CharField(max_length=255, null=True, blank=True)
    vendor_registration_name = models.CharField(max_length=255, null=True, blank=True)

    # ---------- SPECIALITIES ----------
    medical_specialties = models.ManyToManyField(MasterSpeciality, blank=True)

    # ---------- OTHER ----------
    mou_signed = models.BooleanField(default=False)
    mou_received_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.sp_code:
            last = ServiceProvider.objects.order_by("id").last()
            next_id = (last.id + 1) if last else 1
            self.sp_code = f"SP{next_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.center_name


# =====================================================
# SPOC
# =====================================================
class SPOC(BaseModel):
    provider = models.ForeignKey(
        ServiceProvider, related_name="spocs", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)


# =====================================================
# RECOGNITION & MANPOWER
# =====================================================
class ProviderRecognition(BaseModel):
    provider = models.OneToOneField(
        ServiceProvider, related_name="recognition", on_delete=models.CASCADE
    )
    recognitions = models.ManyToManyField("Recognition")
    accreditations = models.ManyToManyField("Accreditation")


class ProviderManpower(BaseModel):
    provider = models.OneToOneField(
        ServiceProvider, related_name="manpower", on_delete=models.CASCADE
    )
    full_time_doctors = models.IntegerField(default=0)
    visiting_doctors = models.IntegerField(default=0)


# =====================================================
# DEPARTMENT CONTACTS
# =====================================================
class DepartmentContact(BaseModel):
    provider = models.ForeignKey(
        ServiceProvider, related_name="department_contacts", on_delete=models.CASCADE
    )
    department = models.CharField(max_length=200)
    title = models.CharField(
        max_length=10,
        choices=[
            ("Dr.", "Dr."),
            ("Mr.", "Mr."),
            ("Ms.", "Ms."),
            ("Mrs.", "Mrs."),
        ]
    )
    contact_person_name = models.CharField(max_length=150, null=True, blank=True)
    designation = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cell_no = models.CharField(max_length=20, null=True, blank=True)


# =====================================================
# SERVICES
# =====================================================
class ProviderService(BaseModel):
    provider = models.OneToOneField(
        ServiceProvider, related_name="service", on_delete=models.CASCADE
    )
    service_categories = models.ManyToManyField(ServiceCategory)

    ambulance = models.CharField(
        max_length=20,
        choices=[
            ("In House", "In House"),
            ("Outsourced", "Outsourced"),
            ("No", "No"),
        ]
    )

    ambulance_type = models.CharField(
        max_length=20,
        choices=[
            ("BLS", "BLS"),
            ("ACLS", "ACLS"),
            ("NA", "NA"),
        ]
    )

    health_checkup = models.BooleanField(default=False)
    bls_ambulances = models.IntegerField(default=0)
    acls_ambulances = models.IntegerField(default=0)


# =====================================================
# RADIOLOGY
# =====================================================
class RadiologyItem(BaseModel):
    provider = models.ForeignKey(
        ServiceProvider, related_name="radiologies", on_delete=models.CASCADE
    )
    radiology_type = models.ForeignKey(RadiologyType, on_delete=models.PROTECT)

    status = models.CharField(
        max_length=3,
        choices=[("Yes", "Yes"), ("No", "No")],
        default="No"
    )

    service_mode = models.CharField(
        max_length=20,
        choices=[
            ("In House", "In House"),
            ("Outsourced", "Outsourced"),
            ("NA", "NA"),
        ],
        default="NA"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)


# =====================================================
# BANK DETAILS
# =====================================================
class BankDetails(BaseModel):
    provider = models.OneToOneField(
        ServiceProvider, related_name="bank", on_delete=models.CASCADE
    )
    account_number = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20)


# =====================================================
# DISCOUNTS & VOUCHERS
# =====================================================
class ProviderDiscount(BaseModel):
    provider = models.ForeignKey(
        ServiceProvider, related_name="discounts", on_delete=models.CASCADE
    )
    discount_service = models.ForeignKey(DiscountService, on_delete=models.PROTECT)
    discount_type = models.CharField(max_length=50)
    discount_id = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active"
    )


class ProviderVoucher(BaseModel):
    provider = models.ForeignKey(
        ServiceProvider, related_name="vouchers", on_delete=models.CASCADE
    )
    voucher_discount = models.ForeignKey(
        VoucherDiscountType, on_delete=models.PROTECT
    )
    voucher_type = models.CharField(max_length=50)
    voucher_id = models.CharField(max_length=50)
    voucher_code = models.CharField(max_length=50)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active"
    )
