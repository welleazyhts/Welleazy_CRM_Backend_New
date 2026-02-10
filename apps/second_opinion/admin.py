from django.contrib import admin
from .models import SecondOpinionCase

admin.site.register(SecondOpinionCase)
class SecondOpinionCaseAdmin(admin.ModelAdmin):
    list_display = (
        'application_number',
        'customer_name',
        'policy_number',
        'created_at',
        'is_active'
    )
