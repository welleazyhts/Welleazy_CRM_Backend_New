from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import (
    Doctor,
    DoctorServicePrice,
    DoctorAvailability,
    DoctorDocument,
    DoctorBankDetail,
    DAY_CHOICES
)
from .serializers import DoctorSerializer



class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'doctor_id'

    # ---------------- CREATE ----------------
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data

        doctor = Doctor.objects.create(
            doctor_name=data['doctor_name'],
            mobile_no=data['mobile_no'],
            alternate_contact=data['alternate_contact'],
            email_id=data['email_id'],
            registration_no=data['registration_no'],
            pan_card=data['pan_card'],
            address=data['address'],
            area=data['area'],
            state_id=data['state'],
            city_id=data['city'],
            pincode=data['pincode'],
            empanel_for_id=data['empanel_for'],
            meet_location_id=data['meet_location'],
            experience_years=data['experience_years'],
            doctor_type_id=data['doctor_type'],
            is_active=data.get('is_active', True),
            is_document_pending=data.get('is_document_pending', False),
        )

        doctor.languages.set(data.get('languages', []))
        doctor.qualifications.set(data.get('qualifications', []))
        doctor.specializations.set(data.get('specializations', []))

        # Services
        for s in data.get('services', []):
            DoctorServicePrice.objects.create(
                doctor=doctor,
                
              
                service_id=s['service_name'],
                price=s['price']
            )

        # Availability (copy logic)
        for a in data.get('availability', []):
            if a.get('copy_time_from_montosun'):
                for day, _ in DAY_CHOICES:
                    DoctorAvailability.objects.update_or_create(
                        doctor=doctor,
                        day=day,
                        shift=a['shift'],
                        defaults={
                            'from_time': a['from_time'],
                            'to_time': a['to_time'],
                            'copy_time_from_montosun': True
                        }
                    )
            else:
                DoctorAvailability.objects.create(doctor=doctor, **a)

        # Documents
        for d in data.get('documents', []):
            DoctorDocument.objects.create(
                doctor=doctor,
                document_type_id=d['document_type'],
                document_file=d['document_file']
            )

        # Bank
        DoctorBankDetail.objects.create(
            doctor=doctor,
            **data['bank']
        )

        return Response(
            self.get_serializer(doctor).data,
            status=status.HTTP_201_CREATED
        )

    # ---------------- UPDATE ----------------
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        doctor = self.get_object()
        data = request.data

        for field in [
            'doctor_name', 'mobile_no', 'alternate_contact', 'email_id',
            'registration_no', 'pan_card', 'address',
            'area', 'pincode', 'experience_years',
            'is_active', 'is_document_pending'
        ]:
            setattr(doctor, field, data.get(field, getattr(doctor, field)))

        doctor.state_id = data.get('state', doctor.state_id)
        doctor.city_id = data.get('city', doctor.city_id)
        doctor.empanel_for_id = data.get('empanel_for', doctor.empanel_for_id)
        doctor.meet_location_id = data.get('meet_location', doctor.meet_location_id)
        doctor.doctor_type_id = data.get('doctor_type', doctor.doctor_type_id)

        doctor.save()

        doctor.languages.set(data.get('languages', doctor.languages.all()))
        doctor.qualifications.set(data.get('qualifications', doctor.qualifications.all()))
        doctor.specializations.set(data.get('specializations', doctor.specializations.all()))

        DoctorServicePrice.objects.filter(doctor=doctor).delete()
        for s in data.get('services', []):
            DoctorServicePrice.objects.create(
                doctor=doctor,
                service_id=s['service_name'],
                price=s['price']
            )

        DoctorAvailability.objects.filter(doctor=doctor).delete()
        for a in data.get('availability', []):
            if a.get('copy_time_from_montosun'):
                for day, _ in DAY_CHOICES:
                    DoctorAvailability.objects.create(
                        doctor=doctor,
                        day=day,
                        shift=a['shift'],
                        from_time=a['from_time'],
                        to_time=a['to_time'],
                        copy_time_from_montosun=True
                    )
            else:
                DoctorAvailability.objects.create(doctor=doctor, **a)

        DoctorDocument.objects.filter(doctor=doctor).delete()
        for d in data.get('documents', []):
            DoctorDocument.objects.create(
                doctor=doctor,
                document_type_id=d['document_type'],
                document_file=d['document_file']
            )

        DoctorBankDetail.objects.update_or_create(
            doctor=doctor,
            defaults=data['bank']
        )

        return Response(self.get_serializer(doctor).data)

    # ---------------- DELETE ----------------
    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
