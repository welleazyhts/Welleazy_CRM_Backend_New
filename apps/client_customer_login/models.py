from django.db import models
from apps.core.models import BaseModel
from apps.accounts.models import User
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.client_customer.models import ClientCustomer
from apps.master_management.models import MasterSubPermission

class ClientLogin(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_login')
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='logins')
    branch = models.ForeignKey(ClientBranch, on_delete=models.SET_NULL, null=True, blank=True, related_name='logins')
    employee = models.ForeignKey(ClientCustomer, on_delete=models.CASCADE, related_name='logins')
    
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(MasterSubPermission, blank=True, related_name='client_logins')

    def __str__(self):
        return f"{self.user.email} - {self.client.corporate_name}"
    
    class Meta:
        db_table = "client_customer_logins"
