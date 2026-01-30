from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_masters.models import BranchZone
from apps.master_management.models import State, City
# from apps.master_management.models import MasterLoginType

class ClientBranch(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='branches')
    # login_type = models.ForeignKey(MasterLoginType, on_delete=models.SET_NULL, null=True, blank=True)
    branch_name = models.CharField(max_length=255)
    spoc_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    email_id = models.EmailField()
    branch_zone = models.ForeignKey(BranchZone, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     if not self.login_type:
    #         branch_type = MasterLoginType.objects.filter(name__iexact="Branch").first()
    #         if branch_type:
    #             self.login_type = branch_type
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.branch_name} ({self.client.corporate_name})"
    
    class Meta:
        db_table = "client_branches"
