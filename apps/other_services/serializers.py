from rest_framework import serializers
from .models import CareProgram

class CareProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareProgram
        fields = [
            'id',
            'care_program_name',
            'normal_price',
            'care_program_details',
            'image',
            'is_active',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'deleted_at'
        ]
