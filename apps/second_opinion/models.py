from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_customer.models import ClientCustomer
from apps.master_management.models import (
    MasterGender,
    MasterRelationship,
    State,
    City,
    MasterInsuranceCompany
)


class SecondOpinionCase(BaseModel):
    class CaseType(models.TextChoices):
        INTERPRETATION = 'Interpretation', 'Interpretation'
        DIGITIZATION = 'Digitization', 'Digitization'

    class InterpretationType(models.TextChoices):
        ECG = 'ECG', 'ECG'
        TMT = 'TMT', 'TMT'

    class ReceivedMode(models.TextChoices):
        INSURER = 'Insurer', 'Insurer'
        EMAIL = 'Email', 'Email'
        SMS = 'SMS', 'SMS'
        FTP = 'FTP', 'FTP'

    # Case Information
    case_type = models.CharField(max_length=50, choices=CaseType.choices)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    client_customer = models.ForeignKey(ClientCustomer, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Customer Details
    customer_name = models.CharField(max_length=200, blank=True, null=True) 
    gender = models.ForeignKey(MasterGender, on_delete=models.SET_NULL, null=True, blank=True)
    relationship = models.ForeignKey(MasterRelationship, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Policy Details
    application_number = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    insurance_company = models.ForeignKey(MasterInsuranceCompany, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Location
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Case Processing
    case_received_mode = models.CharField(max_length=50, choices=ReceivedMode.choices, null=True, blank=True)
    interpretation_type = models.CharField(max_length=50, choices=InterpretationType.choices, null=True, blank=True)
    
    remark = models.TextField(blank=True, null=True)

    report_file = models.FileField(
        upload_to='second_opinion/reports/',
        null=True,
        blank=True
    )

    class CaseStatus(models.TextChoices):
        UNASSIGNED = 'Unassigned', 'Unassigned'
        ASSIGNED = 'Assigned', 'Assigned'
        IN_PROCESS = 'In Process', 'In Process'
        INCOMPLETE_REPORT = 'Incomplete Report', 'Incomplete Report'
        COMPLETED = 'Completed', 'Completed'
        DOCTOR_TAT = 'Doctor TAT', 'Doctor TAT'

    case_status = models.CharField(
        max_length=50, 
        choices=CaseStatus.choices, 
        default=CaseStatus.UNASSIGNED
    )
    
    doctor = models.ForeignKey(
        'doctor.Doctor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    qc_executive = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='second_opinion_qc_cases'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.application_number
