from rest_framework import serializers
from .models import LeadSource, LeadStatus, Lead


class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSource
        fields = '__all__'


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadStatus
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='lead_source.name', read_only=True)
    status_name = serializers.CharField(source='lead_status.name', read_only=True)
    gender_name = serializers.CharField(source='gender.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if obj.lead_type == 'Individual':
            return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        return obj.company_name or ''

    class Meta:
        model = Lead
        fields = '__all__'


class LeadPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def validate(self, data):
        if data.get('lead_type') == 'Individual' and not data.get('gender'):
            raise serializers.ValidationError({
                'gender': 'Gender is required for individual leads.'
            })
        return data
