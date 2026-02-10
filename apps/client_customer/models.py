from django.db import models
from apps.core.models import BaseModel
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.master_management.models import (
    MasterProduct, MasterProductSubCategory, State, City, 
    MasterGender, MasterRelationship
)
from apps.client_masters.models import BranchZone
from apps.test_package.models import TestPackage

class ClientCustomer(BaseModel):
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )

    ADDRESS_TYPE_CHOICES = (
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Other', 'Other'),
    )

    member_id = models.CharField(max_length=50, unique=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='customers')
    branch = models.ForeignKey(ClientBranch, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    product = models.ForeignKey(MasterProduct, on_delete=models.SET_NULL, null=True, blank=True)
    
    packages = models.ManyToManyField(TestPackage, blank=True)
    employee_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    email_id = models.EmailField()
    
    mobile_no = models.CharField(max_length=20)
    gender = models.ForeignKey(MasterGender, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    area_locality = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    
    geo_location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    members_sponsored = models.CharField(max_length=255, blank=True, null=True)
    
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    two_fa_enabled = models.BooleanField(default=False)
    
    account_activation_url = models.URLField(blank=True, null=True)
    last_active_date = models.DateTimeField(blank=True, null=True)
    last_inactive_date = models.DateTimeField(blank=True, null=True)
    inactive_reason = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    services = models.ManyToManyField(MasterProductSubCategory, blank=True)
    next_medical_period = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.member_id:
            last_customer = ClientCustomer.objects.order_by('id').last()
            if last_customer and last_customer.member_id.startswith('EMP'):
                try:
                    last_id = int(last_customer.member_id.replace('EMP', ''))
                    new_id = last_id + 1
                    self.member_id = f"EMP{new_id:06d}"
                except ValueError:
                    self.member_id = "EMP000001"
            else:
                self.member_id = "EMP000001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} ({self.member_id})"

    class Meta:
        db_table = "client_customers"


class ClientCustomerAddress(BaseModel):
    customer = models.ForeignKey(ClientCustomer, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=100, choices=ClientCustomer.ADDRESS_TYPE_CHOICES, blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    area_locality = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    relation_type = models.ForeignKey(MasterRelationship, on_delete=models.SET_NULL, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"Address for {self.customer.customer_name}"

    class Meta:
        db_table = "client_customer_addresses"


class ClientCustomerDependent(BaseModel):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    MARITAL_STATUS_CHOICES = (
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Single', 'Single'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )

    customer = models.ForeignKey(ClientCustomer, on_delete=models.CASCADE, related_name='dependents')
    name = models.CharField(max_length=255)
    relationship = models.ForeignKey(MasterRelationship, on_delete=models.SET_NULL, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    gender = models.ForeignKey(MasterGender, on_delete=models.SET_NULL, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    access_profile_permission = models.BooleanField(default=False)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    member_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    dependent_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):
        if not self.pk:
            count = ClientCustomerDependent.objects.filter(customer=self.customer).count() + 1
            # Dependent Code based on Employee Code
            if self.customer.employee_code:
                self.dependent_id = f"{self.customer.employee_code}ID{count}"
            # Dependent Member ID based on Parent Member ID
            if self.customer.member_id:
                self.member_id = f"{self.customer.member_id}D{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Dependent of {self.customer.customer_name})"

    class Meta:
        db_table = "client_customer_dependents"
