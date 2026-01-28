from rest_framework import serializers
from .models import *


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = "__all__"


class HealthConcernTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthConcernType
        fields = "__all__"


class PlanCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCategory
        fields = "__all__"

class CheckUpTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckUpType
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"