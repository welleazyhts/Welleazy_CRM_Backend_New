from django.db import models
from apps.core.models import BaseModel
from apps.location.models import City

# Create your models here.


# Diagnostic Center Model


class DiagnosticCenter(BaseModel):
    PROVIDER_TYPE_CHOICES = [
        ('clinic', 'Clinic'),
        ('hospital', 'Hospital'),
        ('standalonelab', 'Standalone Lab'),
        ('collectioncenter', 'Collection Center'),
        ('imagingcenter', 'Imaging Center'),
    ]

    GRADE_CHOICES = [
        ('A', 'Grade A - Premium'),
        ('B', 'Grade B - Standard'),
        ('C', 'Grade C - Basic'),
    ]

    name = models.CharField(max_length=255)
    center_code = models.CharField(max_length=100, unique=True)
    unique_name = models.CharField(max_length=255, unique=True)
    token_id = models.CharField(max_length=100, blank=True, null=True)

    provider_type = models.CharField(max_length=50, choices=PROVIDER_TYPE_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    vendor = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

# Diagnostic location Model

class DiagnosticLocation(BaseModel):
    center = models.OneToOneField(DiagnosticCenter, on_delete=models.CASCADE, related_name="location")

    address = models.TextField()
    area = models.CharField(max_length=255)
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="diagnostic_locations",
        null=False,
        blank=False
    )
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)

    work_start = models.TimeField()
    work_end = models.TimeField()
    open_on_sunday = models.BooleanField(default=False)


# Diagnostic Services Model


class DiagnosticServices(BaseModel):
    center = models.OneToOneField(DiagnosticCenter, on_delete=models.CASCADE)

    home_collection = models.BooleanField(default=False)
    home_collection_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_area = models.TextField(blank=True, null=True)

    health_checkup = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)
    home_delivery = models.BooleanField(default=False)


# Diagnostic Capabalities Model


class DiagnosticLabCapabilities(BaseModel):
    center = models.OneToOneField(DiagnosticCenter, on_delete=models.CASCADE)

    hematology = models.BooleanField(default=False)
    biochemistry = models.BooleanField(default=False)
    microbiology = models.BooleanField(default=False)
    pathology = models.BooleanField(default=False)
    serology = models.BooleanField(default=False)
    histopathology = models.BooleanField(default=False)
    endocrinology = models.BooleanField(default=False)
    cytology = models.BooleanField(default=False)
    immunology = models.BooleanField(default=False)
    # Imaging Equipments---

    xray = models.BooleanField(default=False)
    digital_xray = models.BooleanField(default=False)
    ultrasound = models.BooleanField(default=False)
    color_doppler = models.BooleanField(default=False)
    mammogram = models.BooleanField(default=False)
    ct_scan = models.BooleanField(default=False)
    mri = models.BooleanField(default=False)
    pet_scan = models.BooleanField(default=False)
    nuclear_imaging = models.BooleanField(default=False)

    # Cardiac Equipments---

    ecg = models.BooleanField(default=False)
    pft = models.BooleanField(default=False)
    tmt = models.BooleanField(default=False)
    _2d_echo = models.BooleanField(default=False)
    fluoroscopy = models.BooleanField(default=False)


# Diagnostic Staff Model

class DiagnosticStaff(BaseModel):
    center = models.OneToOneField(
        DiagnosticCenter,
        on_delete=models.CASCADE,
        related_name="staff"
    )

    total_staff = models.PositiveIntegerField(default=0)
    doctor_consultants = models.PositiveIntegerField(default=0)
    visiting_consultants = models.PositiveIntegerField(default=0)

    ambulance_available = models.BooleanField(default=False)

    bls_ambulance_count = models.PositiveIntegerField(default=0)
    acls_ambulance_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # If ambulance is not available, reset counts
        if not self.ambulance_available:
            self.bls_ambulance_count = 0
            self.acls_ambulance_count = 0
        super().save(*args, **kwargs)


# Diagnostic Accreditation Model


class DiagnosticAccreditation(BaseModel):
    center = models.OneToOneField(DiagnosticCenter, on_delete=models.CASCADE)

    nabl = models.BooleanField(default=False)
    cap = models.BooleanField(default=False)
    iso = models.BooleanField(default=False)
    iso_type = models.CharField(max_length=100 )

    recognized_by = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)


# Diagnostic Banking Model

class DiagnosticBanking(BaseModel):
    center = models.OneToOneField(DiagnosticCenter, on_delete=models.CASCADE)

    account_holder = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20)

    gst_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=20)


# Diagnostic Agreement Model

class DiagnosticAgreement(BaseModel):
    center = models.OneToOneField(
        DiagnosticCenter,
        on_delete=models.CASCADE,
        related_name="agreement"
    )

    mou_signed = models.BooleanField(default=False)
    mou_signed_date = models.DateField(null=True, blank=True)

    assigned_clients = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # If MOU not signed, clear the date
        if not self.mou_signed:
            self.mou_signed_date = None
        super().save(*args, **kwargs)




