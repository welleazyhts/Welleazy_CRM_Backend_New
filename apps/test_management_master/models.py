from django.db import models
from apps.core.models import BaseModel

# Create your models here.



class TestType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class HealthConcernType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlanCategory(BaseModel):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class CheckUpType(BaseModel):
    name=models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Gender(BaseModel):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
