from django.db import models

# Create your models here.


from django.db import models
from apps.core.models import BaseModel




class PartnershipType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SpecialtyType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class OwnershipType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DCUniqueName(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class ServiceCategory(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class RadiologyType(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class DiscountService(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class VoucherDiscountType(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class PaymentTerm(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class DepartmentType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



#DUMMY MODELS TO BE DELETED LATER-----



    
class Client(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


