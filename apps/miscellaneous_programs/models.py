from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.client_customer.models import ClientCustomer, ClientCustomerDependent
from apps.master_management.models import State, City, CaseStatus, MasterRelationship

class MiscellaneousProgramCase(BaseModel):

    CARE_PROGRAM_CHOICES = (
        ('Gym Service', 'Gym Service'),
    )

    case_id = models.CharField(max_length=20, unique=True, editable=False)
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='misc_cases')
    branch = models.ForeignKey(ClientBranch, on_delete=models.CASCADE, related_name='misc_cases')
    
    employee = models.ForeignKey(ClientCustomer, on_delete=models.CASCADE, related_name='misc_cases')
    case_for = models.ForeignKey(MasterRelationship, on_delete=models.SET_NULL, null=True, blank=True, related_name='misc_cases')
    
    relationship_person = models.ForeignKey(ClientCustomerDependent, on_delete=models.SET_NULL, null=True, blank=True, related_name='misc_cases')
    
    customer_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    email_id = models.EmailField()
    
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    
    care_program = models.CharField(max_length=100, choices=CARE_PROGRAM_CHOICES)
    
    case_status = models.ForeignKey(CaseStatus, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.case_id:
            last_case = MiscellaneousProgramCase.objects.all().order_by('id').last()
            if last_case and last_case.case_id.startswith('MISC'):
                try:
                    last_id = int(last_case.case_id.replace('MISC', ''))
                    new_id = last_id + 1
                    self.case_id = f"MISC{new_id:05d}"
                except ValueError:
                    self.case_id = "MISC00001"
            else:
                self.case_id = "MISC00001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.case_id} - {self.customer_name}"

    class Meta:
        db_table = "miscellaneous_program_cases"
        verbose_name = "Miscellaneous Program Case"
        verbose_name_plural = "Miscellaneous Program Cases"
