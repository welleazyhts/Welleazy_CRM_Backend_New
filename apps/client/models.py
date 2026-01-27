from django.db import models
from apps.core.models import BaseModel
from apps.accounts.models import User
from apps.client_masters.models import (
    BusinessType, CorporateType, Source, VisitType, PartnershipStatus,
    ClientAgreementFrom, PaymentFrequency, Designation, WelleazyCRM, MemberRelationType,
    EmailNotificationType
)

class Client(BaseModel):
    # Business Info
    business_type = models.ForeignKey(BusinessType, on_delete=models.SET_NULL, null=True, blank=True)
    corporate_code = models.CharField(max_length=100, blank=True, null=True)
    corporate_name = models.CharField(max_length=255)
    corporate_type = models.ForeignKey(CorporateType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Contact Info
    mobile_no = models.CharField(max_length=20)
    landline_no = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.EmailField()
    
    # Address Info
    head_office_address = models.TextField(blank=True, null=True)
    branch_office_addresses = models.TextField(blank=True, null=True) # Can be JSON or comma separated
    
    # Sales/Ops Info
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    referred_by = models.CharField(max_length=255, blank=True, null=True)
    welleazy_crm = models.ForeignKey(WelleazyCRM, on_delete=models.SET_NULL, null=True, blank=True)
    
    sales_manager = models.CharField(max_length=255, blank=True, null=True)
    broker = models.CharField(max_length=255, blank=True, null=True)
    ops_spoc = models.CharField(max_length=255, blank=True, null=True)
    
    # Financial/Legal Info
    service_charges = models.CharField(max_length=255, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    gst_no = models.CharField(max_length=50, blank=True, null=True)
    home_visit_charges = models.CharField(max_length=255, blank=True, null=True)
    account_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Other Info
    channel_partner_id = models.CharField(max_length=100, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    billing_email_address = models.EmailField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True) # Active/Inactive toggle
    
    # Sponsorship Info
    total_sponsored = models.CharField(max_length=255, blank=True, null=True)
    total_non_sponsored = models.CharField(max_length=255, blank=True, null=True)
    is_dependent_sponsored = models.BooleanField(default=False)
    members_sponsored = models.ManyToManyField(MemberRelationType, blank=True)
    
    case_registration_mail_auto_triggered = models.BooleanField(default=False)
    separate_account = models.BooleanField(default=False)
    
    # Visit/Partnership
    visit_type = models.ForeignKey(VisitType, on_delete=models.SET_NULL, null=True, blank=True)
    corporate_partnership_status = models.ForeignKey(PartnershipStatus, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Images
    background_image = models.ImageField(upload_to='client_backgrounds/', blank=True, null=True)
    
    # Agreement
    client_agreement_from = models.ForeignKey(ClientAgreementFrom, on_delete=models.SET_NULL, null=True, blank=True)
    agreement_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    frequency_of_payment = models.ForeignKey(PaymentFrequency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.corporate_name

class ClientSPOC(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='spocs')
    person_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.EmailField()
    receive_email_for = models.ManyToManyField(EmailNotificationType, blank=True)

    def __str__(self):
        return f"{self.person_name} ({self.client.corporate_name})"

class ClientDocument(BaseModel):
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    file = models.FileField(upload_to='client_documents/')
    
    def __str__(self):
        return f"Document for {self.client.corporate_name}"
