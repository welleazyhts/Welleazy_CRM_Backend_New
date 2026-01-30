from django.db import models
from apps.core.models import BaseModel
from apps.master_management.models import MasterLoginType, MasterProduct, MasterProductSubCategory
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
# from apps.sub_client.models import SubClient

class ClientProductService(BaseModel):
    login_type = models.ForeignKey(MasterLoginType, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='product_services')
    # sub_client = models.ForeignKey(SubClient, on_delete=models.CASCADE, related_name='product_services', null=True, blank=True)
    branch = models.ForeignKey(ClientBranch, on_delete=models.CASCADE, related_name='product_services', null=True, blank=True)
    
    product = models.ForeignKey(MasterProduct, on_delete=models.CASCADE)
    services = models.ManyToManyField(MasterProductSubCategory, blank=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client.corporate_name} - {self.product.name}"

    class Meta:
        db_table = "client_product_services"
