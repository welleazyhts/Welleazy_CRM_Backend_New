from django.db import models
from apps.core.models import BaseModel

class BaseMaster(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
# ---------- Case related ----------
class CaseReceivedMode(BaseMaster): 
    pass

class CaseType(BaseMaster): 
    pass

class PaymentType(BaseMaster): 
    pass

class CaseFor(BaseMaster): 
    pass

class PreferredVisitType(BaseMaster): 
    pass

class CaseStatus(BaseMaster): 
    pass


# ---------- Client related ----------

class CustomerType(BaseMaster): 
    pass

class ServiceOffered(BaseMaster): 
    pass


# ---------- Customer related ----------

# ---------- Case detail related ----------
class MedicalTest(BaseMaster): 
    pass


class CustomerProfile(BaseMaster): 
    pass

class DhocPaymentOption(BaseMaster): 
    pass
class CaseForMaster(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
