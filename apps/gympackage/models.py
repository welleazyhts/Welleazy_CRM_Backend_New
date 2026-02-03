from django.db import models

import uuid
from apps.core.models import BaseModel
from apps.master_management.models import GymVendors , City
from apps.test_management_master.models import PlanCategory
# Create your models here.


# MASTER TABLES------



class PackagePriceType(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

# MAIN GYMPACKAGE TABLE----



class GymPackage(BaseModel):

    # Vendor
    vendor_name = models.ForeignKey(GymVendors , on_delete=models.CASCADE)

    # Auto-generated Gym SKU
    gym_sku = models.CharField(max_length=20, unique=True, editable=False)

    # Package details
    package_name = models.CharField(max_length=150)
    plan_category = models.ForeignKey(PlanCategory, on_delete=models.CASCADE)
    package_price = models.ForeignKey(PackagePriceType, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0)

    # Auto-calculated
    discounted_package_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    status = models.BooleanField(default=True)

    package_validity_date = models.DateField()

    package_headline_details = models.CharField(max_length=255, blank=True)
    package_description = models.TextField(blank=True)

    image = models.ImageField(upload_to="gym_packages/")

    
    def save(self, *args, **kwargs):
        # Auto-generate SKU
        if not self.gym_sku:
            self.gym_sku = f"GYM-{uuid.uuid4().hex[:8].upper()}"

        # Discount calculation
        discount_amount = (
            self.actual_price * self.discount_percentage
        ) / 100
        self.discounted_package_price = self.actual_price - discount_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.package_name
