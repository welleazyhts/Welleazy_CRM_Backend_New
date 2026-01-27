from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_masters.models import CorporateType, Source, Designation

class SubClient(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sub_clients')
    name = models.CharField(max_length=255)
    corporate_type = models.ForeignKey(CorporateType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Contact
    mobile_no = models.CharField(max_length=20)
    landline_no = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.EmailField()
    
    # Addresses
    head_office_address = models.TextField(blank=True, null=True)
    branch_office_address = models.TextField(blank=True, null=True)
    
    # Meta
    source = models.CharField(max_length=255, null=True, blank=True)
    lead_by = models.CharField(max_length=255, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Sub of {self.client.corporate_name})"

    class Meta:
        db_table = "sub_clients"

class SubClientSPOC(BaseModel):
    sub_client = models.ForeignKey(SubClient, on_delete=models.CASCADE, related_name='spocs')
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "sub_client_spocs"
