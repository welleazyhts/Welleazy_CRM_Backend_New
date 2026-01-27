from django.db import models
from apps.core.models import BaseModel

class MasterBase(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class BusinessType(MasterBase):
    pass

class CorporateType(MasterBase):
    pass

class Source(MasterBase):
    pass

class VisitType(MasterBase):
    pass

class PartnershipStatus(MasterBase):
    pass

class ClientAgreementFrom(MasterBase):
    pass

class PaymentFrequency(MasterBase):
    pass

class Designation(MasterBase):
    pass

class WelleazyCRM(MasterBase):
    pass

class MemberRelationType(MasterBase):
    pass

class BranchZone(MasterBase):
    pass

class EmailNotificationType(MasterBase):
    pass

