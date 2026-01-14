from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.diagnostic_center.models import DiagnosticCenter


class Case(BaseModel):
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
        ("MOBILE", "Mobile App"),
        ("CRM", "CRM Manual Entry"),
        ("CALL", "Call Center"),
        ("EMAIL", "Email"),
        ("WALKIN", "Walk-in"),
        ("HR", "HR Portal"),
    ]

    CUSTOMER_TYPE = [
        ("INDIVIDUAL", "Individual"),
        ("CORPORATE", "Corporate Employee"),
        ("DEPENDANT", "Dependant"),
        ("VIP", "HNI/VIP"),
    ]

    patient_name = models.CharField(max_length=255)
    patient_phone = models.CharField(max_length=15)
    patient_email = models.EmailField(null=True, blank=True)

    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE)

    corporate = models.ForeignKey("corporates.Corporate", null=True, blank=True, on_delete=models.SET_NULL)
    employee_id = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="NORMAL")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)

class CaseServiceDetails(BaseModel):
    SERVICE_TYPES = [
        ("DIAGNOSTIC", "Diagnostic Test"),
        ("DOCTOR", "Doctor Consultation"),
        ("PHARMACY", "Pharmacy Order"),
        ("PACKAGE", "Health Package"),
        ("SPONSORED", "Sponsored Package"),
        ("EYE", "Eye Care"),
        ("DENTAL", "Dental Care"),
        ("GYM", "Gym/Fitness"),
    ]

    VISIT_TYPE = [
        ("HOME", "Home"),
        ("CENTER", "At Center"),
    ]

    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="service")

    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE)

    vendor = models.ForeignKey("vendors.Vendor", on_delete=models.SET_NULL, null=True)
    diagnostic_center = models.ForeignKey(
    "diagnostic_center.DiagnosticCenter",
    on_delete=models.CASCADE,
    null=True,
    blank=True
)




    scheduled_date = models.DateField(null=True)
    scheduled_time = models.TimeField(null=True)
    address = models.TextField(null=True)
class CaseFinancialDetails(BaseModel):
    PAYMENT_TYPE = [
        ("PREPAID", "Prepaid"),
        ("POSTPAID", "Postpaid"),
        ("CORPORATE", "Corporate Billing"),
        ("INSURANCE", "Insurance"),
        ("COD", "Cash on Delivery"),
    ]

    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="financial")

    payment_type = models.CharField(max_length=30, choices=PAYMENT_TYPE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    home_visit_charge = models.DecimalField(max_digits=10, decimal_places=2)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    employee_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    final_amount = models.DecimalField(max_digits=10, decimal_places=2)

class CaseAdditionalDetails(BaseModel):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="additional")

    received_by_name = models.CharField(max_length=255)
    received_by_phone = models.CharField(max_length=20)
    received_by_email = models.EmailField()
    department = models.CharField(max_length=100)

    followup_date = models.DateField(null=True)
    followup_remark = models.TextField(null=True)

    notes = models.TextField()
    internal_notes = models.TextField()
