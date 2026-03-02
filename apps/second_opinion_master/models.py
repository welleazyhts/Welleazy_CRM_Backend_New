from django.db import models

class BaseMaster(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
class SecondOpinionCaseType(BaseMaster):
    pass
class InterpretationType(BaseMaster):
    pass
class CaseReceivedMode(BaseMaster):
    pass
