from rest_framework import serializers
from .models import (
    Doctor,
    DoctorServicePrice,
    DoctorAvailability,
    DoctorDocument,
    DoctorBankDetail
)

# ---------- CHILD SERIALIZERS ----------

class DoctorServicePriceSerializer(serializers.ModelSerializer):
    service_display_name = serializers.CharField(source='service_name.name', read_only=True)

    class Meta:
        model = DoctorServicePrice
        fields = [
            'id','service_id', 'service_name', 'service_display_name', 'price', 'created_at','updated_at', 'created_by','updated_by', 'deleted_at'
        ]
        read_only_fields = ['service_id']


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'


class DoctorDocumentSerializer(serializers.ModelSerializer):
    document_type_name = serializers.CharField(
        source='document_type.name', read_only=True
    )

    class Meta:
        model = DoctorDocument
        fields = '__all__'


class DoctorBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorBankDetail
        fields = '__all__'


# ---------- MAIN DOCTOR SERIALIZER ----------

class DoctorSerializer(serializers.ModelSerializer):
    # FK names
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    empanel_for_name = serializers.CharField(source='empanel_for.name', read_only=True)
    doctor_type_name = serializers.CharField(source='doctor_type.name', read_only=True)
    meet_location_name = serializers.CharField(source='meet_location.name', read_only=True)

    # M2M names
    languages = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    qualifications = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    specializations = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )

    # Children
    services = DoctorServicePriceSerializer(many=True, read_only=True)
    availability = DoctorAvailabilitySerializer(many=True, read_only=True)
    documents = DoctorDocumentSerializer(many=True, read_only=True)
    bank = DoctorBankSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['doctor_id', 'created_at']
