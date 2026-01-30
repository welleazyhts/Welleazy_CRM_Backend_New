from django.db import models

# Create your models here.

from django.db import models
from apps.test_management_master.models import TestType , HealthConcernType
from apps.client.models import Client
from apps.master_management.models import City , MasterVisitType
from apps.core.models import BaseModel

class IndividualTest(BaseModel):

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Disabled", "Disabled"),
    )

    COMPLIMENTARY_CHOICES = (
        ("Complimentary", "Complimentary"),
        ("TBA", "TBA"),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active"
    )

    test_type = models.ForeignKey(TestType, on_delete=models.SET_NULL, null=True)
    visit_type = models.ForeignKey(MasterVisitType, on_delete=models.SET_NULL, null=True)

    product_sku = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    test_name = models.CharField(max_length=255)

    test_code = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    retail_test_price = models.DecimalField(max_digits=10, decimal_places=2)
    corporate_test_price = models.DecimalField(max_digits=10, decimal_places=2)
    hni_test_price = models.DecimalField(max_digits=10, decimal_places=2)

    discount_percent = models.PositiveIntegerField(default=0)
    discount_test_price = models.DecimalField(max_digits=10, decimal_places=2)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    common_test_name = models.CharField(max_length=255, blank=True)

    remark = models.TextField(blank=True)
    test_description = models.TextField(blank=True)

    image = models.ImageField(upload_to="tests/images/", null=True, blank=True)

    complimentary_tba = models.CharField(
        max_length=15,
        choices=COMPLIMENTARY_CHOICES,
        default="TBA"
    )

    health_concern_type = models.ManyToManyField(
        HealthConcernType, blank=True
    )

  

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.product_sku = f"TEST-SKU-{self.id:05d}"
            self.test_code = f"TST-{self.id:05d}"
            super().save(update_fields=["product_sku", "test_code"])

    def __str__(self):
        return self.test_name
