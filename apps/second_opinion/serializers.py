from rest_framework import serializers
from .models import SecondOpinionCase
from apps.client.models import Client
from apps.client_customer.models import ClientCustomer


# Custom field to accept both numeric IDs and string values
class FlexibleChoiceField(serializers.CharField):
    def __init__(self, id_map, **kwargs):
        self.id_map = id_map
        super().__init__(**kwargs)
    
    def to_internal_value(self, data):
        # Convert to string first
        data = str(data) if data is not None else data
        # If it's a numeric ID, convert to the string value
        if data in self.id_map:
            data = self.id_map[data]
        return super().to_internal_value(data)


class SecondOpinionCaseSerializer(serializers.ModelSerializer):
    # ID to String mappings
    CASE_TYPE_MAP = {
        '1': 'Interpretation',
        '2': 'Digitization',
    }
    
    MODE_MAP = {
        '1': 'Insurer',
        '2': 'Email',
        '3': 'SMS',
        '4': 'FTP',
    }
    
    INTERPRETATION_MAP = {
        '1': 'ECG',
        '2': 'TMT',
    }
    
    # Override fields to use custom field class
    case_type = FlexibleChoiceField(id_map=CASE_TYPE_MAP)
    case_received_mode = FlexibleChoiceField(id_map=MODE_MAP, required=False, allow_null=True, allow_blank=True)
    interpretation_type = FlexibleChoiceField(id_map=INTERPRETATION_MAP, required=False, allow_null=True, allow_blank=True)
    class Meta:
        model = SecondOpinionCase
        fields = [
            "id",
            "case_type",
            "client",
            "client_customer",
            "customer_name",
            "gender",
            "relationship",
            "application_number",
            "policy_number",
            "insurance_company",
            "state",
            "city",
            "case_received_mode",
            "interpretation_type",
            "remark",
            "report_file",
            "case_status",
            "doctor",
            "qc_executive",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            'case_type': {'required': True},
            'client': {'required': True},
            'customer_name': {'required': True},
            'application_number': {'required': True},
            'policy_number': {'required': True},
            'remark': {'required': False},
            'report_file': {'required': False},
        }


class SecondOpinionCaseResponseSerializer(serializers.ModelSerializer):
    """Lightweight serializer for API responses"""
    class Meta:
        model = SecondOpinionCase
        fields = [
            "id",
            "case_type",
            "client",
            "customer_name",
            "application_number",
            "policy_number",
            "case_received_mode",
            "interpretation_type",
            "remark",
            "report_file",
            "case_status",
            "created_at",
        ]
        read_only_fields = fields  # All fields are read-only in response

        

class SecondOpinionCaseListSerializer(SecondOpinionCaseSerializer):
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.doctor_name', read_only=True)
    qc_executive_name = serializers.CharField(source='qc_executive.username', read_only=True)
    interpretation_assign_date = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta(SecondOpinionCaseSerializer.Meta):
        fields = SecondOpinionCaseSerializer.Meta.fields + ['client_name', 'doctor_name', 'qc_executive_name', 'interpretation_assign_date']


class SecondOpinionBulkUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    case_type = serializers.IntegerField(required=True)
    client = serializers.IntegerField(required=True)
    
    def validate_file(self, value):
        if not value.name.endswith('.csv') and not value.name.endswith('.xlsx') and not value.name.endswith('.xls'):
            raise serializers.ValidationError("Only CSV or Excel files are allowed.")
        return value


class SecondOpinionAssignDoctorSerializer(serializers.Serializer):
    case_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )
    doctor_id = serializers.IntegerField(required=True)
