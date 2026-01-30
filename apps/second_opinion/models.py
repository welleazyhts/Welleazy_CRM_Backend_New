from django.db import models


class SecondOpinionCase(models.Model):

    customer_name = models.CharField(max_length=200)
    application_number = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)

    remark = models.TextField()

    report_file = models.FileField(
        upload_to='second_opinion/reports/',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application_number
