from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_customer.models import ClientCustomer , ClientCustomerDependent
from apps.client_branch.models import ClientBranch
from apps.master_management.models import MasterRelationship , State , City , CaseStatus
from apps.other_services.models import CareProgram

# Create your models here.


class CareProgramCase(BaseModel):

    case_id = models.CharField(max_length=20, unique=True, editable=False)

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    branch = models.ForeignKey(ClientBranch, on_delete=models.PROTECT)

    # Employee (always Customer)
    employee = models.ForeignKey(
        ClientCustomer,
        on_delete=models.PROTECT,
        related_name='employee_cases'
    )

    # Case For (Self / Father / etc.)
    case_for = models.ForeignKey(
        MasterRelationship,
        on_delete=models.PROTECT
    )

    relationship_person = models.ForeignKey(
        ClientCustomerDependent,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='care_cases'
    )

    # One of these will be used based on case_for
    customer_name= models.CharField(max_length=255)

    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField()

    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    address = models.TextField(blank=True, null=True)

    care_program = models.ForeignKey(
        CareProgram,
        on_delete=models.PROTECT
    )

    case_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT
    )

    requirements = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

   

    def save(self, *args, **kwargs):
        if not self.case_id:
            count = CareProgramCase.objects.count() + 1
            self.case_id = f"WZCP{count:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.case_id
