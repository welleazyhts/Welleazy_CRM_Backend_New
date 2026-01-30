from django.db import models

# Create your models here.

import uuid
from django.db import models
from apps.doctor_master.models import *
from apps.master_management.models import DoctorLanguage , DoctorQualification , DoctorSpecialization , State , City
from apps.core.models import BaseModel

def generate_doctor_id():
    return f"DCWZ{uuid.uuid4().hex[:6].upper()}"


class Doctor(BaseModel):
    doctor_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        default=generate_doctor_id
    )

    doctor_name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=15)
    alternate_contact = models.CharField(max_length=15)
    email_id = models.EmailField()

    languages = models.ManyToManyField(DoctorLanguage)
    qualifications = models.ManyToManyField(DoctorQualification)
    specializations = models.ManyToManyField(DoctorSpecialization)

    registration_no = models.CharField(max_length=100)
    pan_card = models.CharField(max_length=20)

    address = models.TextField()
    area = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.CharField(max_length=10)

    empanel_for = models.ForeignKey(EmpanelFor, on_delete=models.PROTECT)
    meet_location = models.ForeignKey(MeetLocation, on_delete=models.PROTECT)
    experience_years = models.PositiveIntegerField()
    doctor_type = models.ForeignKey(DoctorType, on_delete=models.PROTECT)

    is_active = models.BooleanField(default=True)
    is_document_pending = models.BooleanField(default=False)

  

    def __str__(self):
        return f"{self.doctor_id} - {self.name}"


def generate_service_id():
    return uuid.uuid4().hex[:6].upper()


class DoctorServicePrice(models.Model):
    service_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        default=generate_service_id
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='services'
    )
    service_name = models.ForeignKey(EmpanelFor, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_id


DAY_CHOICES = [
    ('mon','Monday'), ('tue','Tuesday'), ('wed','Wednesday'),
    ('thu','Thursday'), ('fri','Friday'), ('sat','Saturday'), ('sun','Sunday')
]

SHIFT_CHOICES = [
    ('morning','Morning'),
    ('evening','Evening'),
    ('night','Night')
]


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='availability'
    )

    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)

    from_time = models.TimeField()
    to_time = models.TimeField()

    copy_time_from_montosun = models.BooleanField(default=False)



class DoctorDocument(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    document_file = models.FileField(upload_to='doctor_documents/')



class DoctorBankDetail(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='bank')
    account_number = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=150)
    branch_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)