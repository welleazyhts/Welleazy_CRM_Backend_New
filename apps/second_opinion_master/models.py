from django.db import models

# Common base (same pattern you already use)
class BaseMaster(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 1️⃣ Case Type dropdown
class SecondOpinionCaseType(BaseMaster):
    pass


# 2️⃣ Interpretation Type dropdown
class InterpretationType(BaseMaster):
    pass
# 3️⃣ Case Received Mode dropdown
class CaseReceivedMode(BaseMaster):
    pass
