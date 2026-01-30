from rest_framework import serializers
from .models import *

class SimpleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name' , 'created_by' , 'updated_by', 'created_at' , 'updated_at' , 'deleted_at']



class EmpanelForSerializer(SimpleSerializer):
    class Meta(SimpleSerializer.Meta):
        model = EmpanelFor


class DoctorTypeSerializer(SimpleSerializer):
    class Meta(SimpleSerializer.Meta):
        model = DoctorType


class MeetLocationSerializer(SimpleSerializer):
    class Meta(SimpleSerializer.Meta):
        model = MeetLocation


class DocumentTypeSerializer(SimpleSerializer):
    class Meta(SimpleSerializer.Meta):
        model = DocumentType