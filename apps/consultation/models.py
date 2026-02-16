from django.db import models
from apps.core.models import BaseModel
from apps.master_management.models import (
    MasterProduct, MasterProductSubCategory, MasterSpecialtiesTest,
    MasterBranch, State, City, MasterLanguage,
    MasterRelationship, CaseStatus
)
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.accounts.models import User
from apps.doctor.models import Doctor
from apps.core.choices import GENDER_CHOICES

class ConsultationCase(BaseModel):
    # Choices
    CASE_REC_MODE_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Call', 'Call'),
        ('Client Online Updations', 'Client Online Updations'),
        ('Client Sales Person Updations', 'Client Sales Person Updations'),
        ('Customer Online Updations', 'Customer Online Updations'),
    ]
    CUSTOMER_TYPE_CHOICES = [
        ('New', 'New'),
        ('Registered', 'Registered'),
    ]
    CASE_FOR_CHOICES = [
        ('Self', 'Self'),
        ('Dependent', 'Dependent'),
        ('Both', 'Both')
    ]
    CUSTOMER_PROFILE_CHOICES = [
        ('Normal', 'Normal'),
        ('HNI', 'HNI'),
        ('NRI', 'NRI'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('Corporate Paid', 'Corporate Paid'),
        ('Customer Paid', 'Customer Paid'),
    ]
    PAYMENT_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
    ]
    PAYING_TO_CHOICES = [
        ('Welleazy', 'Welleazy'),
        ('DC/Hospital', 'DC/Hospital'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Received', 'Received'),
        ('Pending', 'Pending'),
    ]
    APPOINTMENT_STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Pending', 'Pending'),
        ('Rescheduled', 'Rescheduled'),
    ]
    SPONSOR_STATUS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Partial', 'Partial'),
    ]
    CASE_TYPE_CHOICES = [
        ('Main', 'Main'),
        ('Additional', 'Additional'),
    ]

    consultation_type = models.ForeignKey(MasterProduct, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    service = models.ForeignKey(MasterProductSubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    specialities_test_list = models.ForeignKey(MasterSpecialtiesTest, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    
    case_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    case_rec_mode = models.CharField(max_length=50, choices=CASE_REC_MODE_CHOICES, default='Email')
    case_rec_date_time = models.DateTimeField(null=True, blank=True)
    welleazy_branch = models.ForeignKey(MasterBranch, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    # assigned_executive = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_consultation_cases')
    assigned_executive = models.CharField(max_length=255, blank=True, null=True)

    corporate_name = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    branch_name = models.ForeignKey(ClientBranch, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    customer_type = models.CharField(max_length=50, choices=CUSTOMER_TYPE_CHOICES, default='New')
    members_sponsored = models.CharField(max_length=255, blank=True, null=True)
    received_by_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True) 
    email_id = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    channel_partner_name = models.CharField(max_length=255, blank=True, null=True)
    channel_partner_id = models.CharField(max_length=100, blank=True, null=True)
    case_for = models.CharField(max_length=50, choices=CASE_FOR_CHOICES, default='Self')

    customer_name = models.CharField(max_length=255)
    customer_mobile = models.CharField(max_length=20)
    alternate_number = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    preferred_language = models.ForeignKey(MasterLanguage, on_delete=models.SET_NULL, null=True, blank=True)
    sponsor_status = models.CharField(max_length=100, choices=SPONSOR_STATUS_CHOICES, blank=True, null=True)
    no_of_free_consultations = models.PositiveIntegerField(default=0)
    no_of_consultations_used = models.PositiveIntegerField(default=0)

    application_no = models.CharField(max_length=100, blank=True, null=True)
    customer_profile = models.CharField(max_length=50, choices=CUSTOMER_PROFILE_CHOICES, default='Normal')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES, default='Corporate Paid')

    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=250.00)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES, blank=True, null=True)
    paying_to = models.CharField(max_length=50, choices=PAYING_TO_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_received_date_time = models.DateTimeField(null=True, blank=True)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)



    case_status = models.ForeignKey(CaseStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_cases')
    follow_up_date_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.case_id:
            last_case = ConsultationCase.objects.filter(case_id__startswith='WX').order_by('-case_id').first()
            if last_case:
                try:
                    last_id_numeric = int(last_case.case_id.replace('WX', ''))
                    new_id_numeric = last_id_numeric + 1
                    self.case_id = f"WX{new_id_numeric:05d}"
                except ValueError:
                    self.case_id = "WX00001"
            else:
                count = ConsultationCase.objects.all().count()
                self.case_id = f"WX{count + 1:05d}"

        if not self.id and self.consultation_type:
            if self.consultation_type.name == "Comprehensive Services":
                if self.payable_amount == 250.00: 
                    self.payable_amount = 499.00
            else:
                if self.payable_amount == 499.00:
                    self.payable_amount = 250.00
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Case {self.id} - {self.customer_name}"

    class Meta:
        db_table = 'consultation_cases'
        ordering = ['-created_at']

class ConsultationDoctorDetails(BaseModel):
    case = models.ForeignKey(ConsultationCase, on_delete=models.CASCADE, related_name='doctor_details')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation_doctor_details')
    preferred_language = models.ForeignKey(MasterLanguage, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=ConsultationCase.APPOINTMENT_STATUS_CHOICES, default='Scheduled')
    case_status = models.ForeignKey(CaseStatus, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Doctor Details for Case {self.case.id} with {self.doctor.doctor_name if self.doctor else 'Unassigned'}"

class ConsultationCaseDependent(BaseModel):
    case = models.ForeignKey(ConsultationCase, on_delete=models.CASCADE, related_name='dependents')
    
    person_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    relationship = models.ForeignKey(MasterRelationship, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_mode = models.CharField(max_length=50, choices=ConsultationCase.PAYMENT_MODE_CHOICES, blank=True, null=True)
    paying_to = models.CharField(max_length=50, choices=ConsultationCase.PAYING_TO_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=ConsultationCase.PAYMENT_STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_received_date_time = models.DateTimeField(null=True, blank=True)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    case_type = models.CharField(max_length=50, choices=ConsultationCase.CASE_TYPE_CHOICES, blank=True, null=True) 
    preferred_language = models.ForeignKey(MasterLanguage, on_delete=models.SET_NULL, null=True, blank=True)
    
    follow_up_date_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dependent {self.person_name} for Case {self.case.id}"

    class Meta:
        db_table = 'consultation_case_dependents'
        ordering = ['created_at']

class ConsultationCaseDocument(BaseModel):
    case = models.ForeignKey(ConsultationCase, on_delete=models.CASCADE, related_name='documents')
    document_file = models.FileField(upload_to='consultation/documents/')
    document_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Document for Case {self.case.id}: {self.document_name or self.document_file.name}"

    class Meta:
        db_table = 'consultation_case_documents'
        ordering = ['created_at']
