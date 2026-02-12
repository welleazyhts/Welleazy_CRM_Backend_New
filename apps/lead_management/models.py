from django.db import models
from apps.core.models import BaseModel
from apps.master_management.models import (
    State, City, MasterTypeOfInsurance,
    MasterInsuranceCompany
)
from apps.core.choices import GENDER_CHOICES


class LeadSource(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'lead_sources'
        verbose_name_plural = 'Lead Sources'


class LeadStatus(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'lead_status'
        verbose_name_plural = 'Lead Statuses'


class Lead(BaseModel):

    LEAD_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Corporate', 'Corporate'),
    ]
    
    SERVICE_TYPE_CHOICES = [
        ('Health Care', 'Health Care'),
        ('Insurance', 'Insurance'),
        ('Others', 'Others'),
    ]
    
    SERVICE_CATEGORY_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Insurance Records', 'Insurance Records'),
        ('Diagnostics', 'Diagnostics'),
        ('Health Records', 'Health Records'),
    ]
    
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES, default='Individual')
    lead_owner = models.CharField(max_length=255, blank=True, null=True)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    
    phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    company_name = models.CharField(max_length=255, blank=True, null=True)
    website_name = models.URLField(blank=True, null=True)
    no_of_employees = models.IntegerField(null=True, blank=True)
    
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, blank=True, null=True)
    service_category = models.CharField(max_length=50, choices=SERVICE_CATEGORY_CHOICES, blank=True, null=True)
    
    policy_type = models.ForeignKey(MasterTypeOfInsurance, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    existing_insurer = models.ForeignKey(MasterInsuranceCompany, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    
    reminder_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    
    receive_email = models.BooleanField(default=False)
    receive_sms = models.BooleanField(default=False)
    receive_whatsapp = models.BooleanField(default=False)
    
    remarks = models.TextField(blank=True, null=True)
    upload_document = models.FileField(upload_to='leads/documents/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.lead_type})"
    
    class Meta:
        db_table = 'leads'
        verbose_name_plural = 'Leads'

        ordering = ['-created_at']


class IndividualClient(BaseModel):
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    # Personal Information
    employee_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=100, unique=True)
    contact_no = models.CharField(max_length=20)
    company_email = models.EmailField()
    
    # Company Details
    company_name = models.CharField(max_length=255)
    company_address = models.TextField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Personal Details
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Insurance Information
    type_of_insurance = models.ForeignKey(
        MasterTypeOfInsurance, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='individual_clients'
    )
    current_insurer = models.ForeignKey(
        MasterInsuranceCompany, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='individual_clients'
    )
    expiry_date = models.DateField(null=True, blank=True)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sum_assured = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Document and Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    def __str__(self):
        return f"{self.employee_name} ({self.employee_id})"
    
    class Meta:
        db_table = 'individual_clients'
        ordering = ['-created_at']
        verbose_name = 'Individual Client'
        verbose_name_plural = 'Individual Clients'


class IndividualClientDependent(BaseModel):
    
    individual_client = models.ForeignKey(
        IndividualClient, 
        on_delete=models.CASCADE, 
        related_name='dependents'
    )
    name = models.CharField(max_length=255)
    relationship = models.ForeignKey(
        'master_management.MasterRelationship',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        relationship_name = self.relationship.name if self.relationship else 'Unknown'
        return f"{self.name} ({relationship_name}) - {self.individual_client.employee_name}"
    
    class Meta:
        db_table = 'individual_client_dependents'
        ordering = ['individual_client', 'name']
        verbose_name = 'Individual Client Dependent'
        verbose_name_plural = 'Individual Client Dependents'


class IndividualClientDocument(BaseModel):
    individual_client = models.ForeignKey(
        IndividualClient, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    document = models.FileField(upload_to='individual_clients/documents/')
    
    def __str__(self):
        return f"Document for {self.individual_client.employee_name}"
    
    class Meta:
        db_table = 'individual_client_documents'
        verbose_name = 'Individual Client Document'
        verbose_name_plural = 'Individual Client Documents'
