from django.db import models

# Create your models here.



from django.db import models
from apps.test_management_master.models import (
    PlanCategory,
    CheckUpType
)
from apps.test_individual.models import IndividualTest
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.master_management.models import MasterVisitType , City , MasterGender


class TestPackage(BaseModel):

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Disabled", "Disabled"),
    )

    COMPLIMENTARY_CHOICES = (
        ("Complimentary", "Complimentary"),
        ("TBA", "TBA"),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    product_sku = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    package_name = models.CharField(max_length=255)

    plan_category = models.ForeignKey(
        PlanCategory,
        on_delete=models.SET_NULL,
        null=True
    )


    checkup_type = models.ForeignKey(
        CheckUpType,
        on_delete=models.SET_NULL,
        null=True
    )

    visit_type = models.ForeignKey(
        MasterVisitType,
        on_delete=models.SET_NULL,
        null=True
    )

    # ✅ tests included (filtered by client in API)
    tests_included = models.ManyToManyField(
        IndividualTest,
        blank=True
    )

    retail_package_price = models.DecimalField(max_digits=10, decimal_places=2)
    corporate_package_price = models.DecimalField(max_digits=10, decimal_places=2)
    hni_package_price = models.DecimalField(max_digits=10, decimal_places=2)

    discount_percent = models.PositiveIntegerField(default=0)
    discount_package_price = models.DecimalField(max_digits=10, decimal_places=2)

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active"
    )

    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)

    gender = models.ForeignKey(
        MasterGender,
        on_delete=models.SET_NULL,
        null=True
    )

    package_validity_date = models.DateField(null=True, blank=True)

    remark = models.TextField(blank=True)
    package_headline_details = models.CharField(max_length=255, blank=True)
    package_details = models.TextField(blank=True)

    image = models.ImageField(upload_to="packages/images/", null=True, blank=True)
    mer_form = models.FileField(upload_to="packages/mer/", null=True, blank=True)
    fitness_form = models.FileField(upload_to="packages/fitness/", null=True, blank=True)

    complimentary_tba = models.CharField(
        max_length=15,
        choices=COMPLIMENTARY_CHOICES,
        default="TBA"
    )

   

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.product_sku = f"PKG-{self.id:05d}"
            super().save(update_fields=["product_sku"])

    def __str__(self):
        return self.package_name
