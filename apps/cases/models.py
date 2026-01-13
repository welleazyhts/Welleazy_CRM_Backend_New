from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Corporate(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


    class Meta:
        abstract = True


class Case(BaseModel):
    CUSTOMER_TYPE_CHOICES =[
    ("INDIVIDUAL", "Individual"),
    ("CORPORATE_EMPLOYEE", "Corporate Employee"),
    ("DEPENDANT", "Dependant"),
    ("HNI_VIP", "HNI/VIP"),]

    STATUS_CHOICES = [
    ("NEW", "New"),
    ("ASSIGNED", "Assigned"),
    ("IN_PROGRESS", "In Progress"),
    ("SCHEDULED", "Scheduled"),
]
    PRIORITY_CHOICES = [
    ("LOW", "Low"),
    ("NORMAL", "Normal"),
    ("HIGH", "High"),
    ("URGENT", "Urgent"),
]

    SOURCE_CHOICES = [
    ("WEBSITE", "Website"),
    ("MOBILE_APP", "Mobile App"),
    ("CRM_MANUAL", "CRM Manual Entry"),
    ("CALL_CENTER", "Call Center"),
    ("EMAIL", "Email"),
    ("WALK_IN", "Walk-in"),
    ("HR_PORTAL", "HR Portal"),
]

    SERVICE_TYPE_CHOICES = [
    ("HOME_COLLECTION", "Home Collection"),
    ("LAB_VISIT", "Lab Visit"),
    ("DOCTOR_VISIT", "Doctor Visit"),
]

    VISIT_TYPE_CHOICES = [
    ("HOME", "Home"),
    ("CENTER", "Center"),
]

    PAYMENT_TYPE_CHOICES = [
    ("PREPAID", "Prepaid"),
    ("POSTPAID", "Postpaid"),
    ("CORPORATE", "Corporate Billing"),
    ("INSURANCE", "Insurance"),
]

    # BASIC
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="NORMAL")
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    patient_name = models.CharField(max_length=255, null=True, blank=True)
    patient_phone = models.CharField(max_length=20, null=True, blank=True)
    patient_email = models.EmailField(null=True, blank=True)
    corporate = models.CharField(max_length=255, null=True, blank=True)
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    customer_type = models.CharField(
    max_length=30,
    choices=CUSTOMER_TYPE_CHOICES,
    default="INDIVIDUAL"
)

    
    
    customer_type = models.CharField(
    max_length=30,
    choices=CUSTOMER_TYPE_CHOICES,
    default="INDIVIDUAL"
)
   


    
    

    # SERVICE
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    visit_type = models.CharField(max_length=30, choices=VISIT_TYPE_CHOICES)
    vendor = models.CharField(max_length=255, null=True, blank=True)
    diagnostic_center = models.CharField(max_length=255, null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    service_address = models.TextField(null=True, blank=True)

    # FINANCIAL
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    home_visit_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employee_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ADDITIONAL
    received_by_name = models.CharField(max_length=255, null=True, blank=True)
    received_by_phone = models.CharField(max_length=15, null=True, blank=True)
    received_by_email = models.EmailField(null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    followup_date = models.DateField(null=True, blank=True)
    followup_remark = models.TextField(null=True, blank=True)
    customer_notes = models.TextField(null=True, blank=True)
    internal_notes = models.TextField(null=True, blank=True)

   


    

    def save(self, *args, **kwargs):
        self.final_amount = (
            self.total_amount
            - self.discount
            + self.home_visit_charge
            + self.service_charge
            - self.employee_to_pay
        )
        super().save(*args, **kwargs)
