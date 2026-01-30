from django.db import models

# Create your models here.


from apps.core.models import BaseModel


class EmpanelFor(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DoctorType(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MeetLocation(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class DocumentType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name