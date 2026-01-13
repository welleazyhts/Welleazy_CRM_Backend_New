from django.db import models

class Corporate(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "corporates_corporate"

    def __str__(self):
        return self.name
