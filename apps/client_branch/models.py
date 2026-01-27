from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_masters.models import BranchZone
from apps.master_management.models import State, City

class ClientBranch(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=255)
    spoc_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    email_id = models.EmailField()
    branch_zone = models.ForeignKey(BranchZone, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.branch_name} ({self.client.corporate_name})"
    
    class Meta:
        db_table = "client_branches"
