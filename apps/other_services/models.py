from django.db import models

# Create your models here.

from apps.core.models import BaseModel

class CareProgram(BaseModel):
    care_program_name = models.CharField(max_length=255)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    care_program_details = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='care_programs/', null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.care_program_name
