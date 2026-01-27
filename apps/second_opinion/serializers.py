from rest_framework import serializers
from .models import SecondOpinionCase


class SecondOpinionCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondOpinionCase
        fields = [
            "id",
            "customer_name",
            "application_number",
            "policy_number",
            "remark",
            "report_file",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
