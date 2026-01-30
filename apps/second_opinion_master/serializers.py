from rest_framework import serializers
from .models import SecondOpinionCaseType, InterpretationType
from .models import CaseReceivedMode


class BaseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'is_active']


class SecondOpinionCaseTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = SecondOpinionCaseType


class InterpretationTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = InterpretationType

class CaseReceivedModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseReceivedMode
        fields = ["id", "name", "is_active"]
