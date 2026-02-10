from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q

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
    lookup_field = 'id'

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
            created_by=request.user,
        )

        doctor.languages.set(data.get('languages', []))
        doctor.qualifications.set(data.get('qualifications', []))
        doctor.specializations.set(data.get('specializations', []))

        # Services
        for s in data.get('services', []):
            DoctorServicePrice.objects.create(
                doctor=doctor,
                created_by=request.user,
                service_name_id=s['service_name'],
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
                        created_by=request.user,
                        defaults={
                            'from_time': a['from_time'],
                            'to_time': a['to_time'],
                            'copy_time_from_montosun': True
                        }
                    )
            else:
                DoctorAvailability.objects.create(doctor=doctor , created_by=request.user, **a)

        # Documents
        for d in data.get('documents', []):
            DoctorDocument.objects.create(
                doctor=doctor,
                created_by=request.user,
                document_type_id=d['document_type'],
                document_file=d['document_file']
            )

        # Bank
        DoctorBankDetail.objects.create(
            doctor=doctor,
            created_by=request.user,
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

    # ---------------- MAIN DOCTOR ----------------
        for field in [
            'doctor_name', 'mobile_no', 'alternate_contact', 'email_id',
            'registration_no', 'pan_card', 'address',
            'area', 'pincode', 'experience_years',
            'is_active', 'is_document_pending'
        ]:
            if field in data:
                setattr(doctor, field, data[field])

        doctor.state_id = data.get('state', doctor.state_id)
        doctor.city_id = data.get('city', doctor.city_id)
        doctor.empanel_for_id = data.get('empanel_for', doctor.empanel_for_id)
        doctor.meet_location_id = data.get('meet_location', doctor.meet_location_id)
        doctor.doctor_type_id = data.get('doctor_type', doctor.doctor_type_id)
        doctor.updated_by = request.user
        doctor.save()

    # ---------------- M2M ----------------
        if 'languages' in data:
            doctor.languages.set(data['languages'])

        if 'qualifications' in data:
            doctor.qualifications.set(data['qualifications'])

        if 'specializations' in data:
            doctor.specializations.set(data['specializations'])

    # ---------------- SERVICES (UPSERT) ----------------
        existing_service_ids = set(
            DoctorServicePrice.objects.filter(doctor=doctor)
            .values_list('id', flat=True)
        )

        incoming_service_ids = set()

        for s in data.get('services', []):
            service_row_id = s.get('id')

            if service_row_id:
            # UPDATE
                DoctorServicePrice.objects.filter(
                    id=service_row_id,
                    doctor=doctor
                ).update(
                    service_name_id=s['service_name'],
                    price=s['price'],
                    updated_by=request.user
                )
                incoming_service_ids.add(service_row_id)
            else:
            # CREATE
                obj = DoctorServicePrice.objects.create(
                    doctor=doctor,
                    service_name_id=s['service_name'],
                    price=s['price'],
                    created_by=request.user,
                    updated_by=request.user
                )
                incoming_service_ids.add(obj.id)

    # DELETE removed services
        DoctorServicePrice.objects.filter(
            doctor=doctor
        ).exclude(id__in=incoming_service_ids).delete()

    # ---------------- AVAILABILITY (UPSERT + COPY LOGIC) ----------------
        existing_availability_ids = set(
            DoctorAvailability.objects.filter(doctor=doctor)
            .values_list('id', flat=True)
        )

        incoming_availability_ids = set()

        for a in data.get('availability', []):
            avail_id = a.get('id')

            if a.get('copy_time_from_montosun'):
            # remove same shift first
                DoctorAvailability.objects.filter(
                    doctor=doctor,
                    shift=a['shift']
                ).delete()

                for day, _ in DAY_CHOICES:
                    obj = DoctorAvailability.objects.create(
                        doctor=doctor,
                        day=day,
                        shift=a['shift'],
                        from_time=a['from_time'],
                        to_time=a['to_time'],
                        copy_time_from_montosun=True,
                        updated_by=request.user
                    )
                    incoming_availability_ids.add(obj.id)

            elif avail_id:
                # UPDATE
                DoctorAvailability.objects.filter(
                    id=avail_id,
                    doctor=doctor
                ).update(
                    day=a['day'],
                    shift=a['shift'],
                    from_time=a['from_time'],
                    to_time=a['to_time'],
                    updated_by=request.user
                )
                incoming_availability_ids.add(avail_id)

            else:
            # CREATE
                obj = DoctorAvailability.objects.create(
                    doctor=doctor,
                    day=a['day'],
                    shift=a['shift'],
                    from_time=a['from_time'],
                    to_time=a['to_time'],
                    created_by=request.user,
                    updated_by=request.user
                )
                incoming_availability_ids.add(obj.id)

        DoctorAvailability.objects.filter(
            doctor=doctor
        ).exclude(id__in=incoming_availability_ids).delete()

    # ---------------- DOCUMENTS (UPSERT) ----------------
        existing_doc_ids = set(
            DoctorDocument.objects.filter(doctor=doctor)
            .values_list('id', flat=True)
        )

        incoming_doc_ids = set()

        for d in data.get('documents', []):
            doc_id = d.get('id')

            if doc_id:
                DoctorDocument.objects.filter(
                    id=doc_id,
                    doctor=doctor
                ).update(
                    document_type_id=d['document_type'],
                    document_file=d.get('document_file'),
                    updated_by=request.user
                )
                incoming_doc_ids.add(doc_id)
            else:
                obj = DoctorDocument.objects.create(
                    doctor=doctor,
                    document_type_id=d['document_type'],
                    document_file=d['document_file'],
                    updated_by=request.user
                )
                incoming_doc_ids.add(obj.id)

        DoctorDocument.objects.filter(
            doctor=doctor
        ).exclude(id__in=incoming_doc_ids).delete()

    # ---------------- BANK (UPSERT) ----------------
        if 'bank' in data:
            DoctorBankDetail.objects.update_or_create(
                doctor=doctor,
                defaults={**data['bank'], 'updated_by': request.user}
            )

        return Response(self.get_serializer(doctor).data)


    # ---------------- DELETE ----------------
    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        doctor.delete()
        return Response(
            {"message": "Doctor Details deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    

    # FILTERING THE DOCTOR DETAILS---

    
    def get_queryset(self):
        queryset = Doctor.objects.all()
        params = self.request.query_params

        doctor_name = params.get('doctor_name')
        doctor_id = params.get('doctor_id')   # autogenerated DCWZ...
        search = params.get('search')

        if doctor_name:
            queryset = queryset.filter(
                doctor_name__icontains=doctor_name
            )

        if doctor_id:
            queryset = queryset.filter(
                doctor_id__icontains=doctor_id
            )

        # optional single search box
        if search:
            queryset = queryset.filter(
                Q(doctor_name__icontains=search) |
                Q(doctor_id__icontains=search)
            )

        return queryset

        # For updating the perticular data----

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        doctor = self.get_object()
        data = request.data

        # ----------- MAIN DOCTOR FIELDS -----------
        for field in [
            'doctor_name', 'mobile_no', 'alternate_contact', 'email_id',
            'registration_no', 'pan_card', 'address',
            'area', 'pincode', 'experience_years',
            'is_active', 'is_document_pending'
        ]:
            if field in data:
                setattr(doctor, field, data[field])

        # ----------- FK FIELDS -----------
        if 'state' in data:
            doctor.state_id = data['state']
        if 'city' in data:
            doctor.city_id = data['city']
        if 'empanel_for' in data:
            doctor.empanel_for_id = data['empanel_for']
        if 'meet_location' in data:
            doctor.meet_location_id = data['meet_location']
        if 'doctor_type' in data:
            doctor.doctor_type_id = data['doctor_type']

        doctor.updated_by = request.user
        doctor.save()

        # ----------- M2M (ONLY IF SENT) -----------
        if 'languages' in data:
            doctor.languages.set(data['languages'])

        if 'qualifications' in data:
            doctor.qualifications.set(data['qualifications'])

        if 'specializations' in data:
            doctor.specializations.set(data['specializations'])

        # ----------- SERVICES (UPSERT ONLY IF SENT) -----------
        if 'services' in data:
            for s in data['services']:
                service_row_id = s.get('id')

                if service_row_id:
                    DoctorServicePrice.objects.filter(
                        id=service_row_id,
                        doctor=doctor
                    ).update(
                        service_name_id=s['service_name'],
                        price=s['price'],
                        updated_by=request.user
                    )
                else:
                    DoctorServicePrice.objects.create(
                        doctor=doctor,
                        service_name_id=s['service_name'],
                        price=s['price'],
                        updated_by=request.user
                    )

        # ----------- AVAILABILITY (ONLY IF SENT) -----------
        if 'availability' in data:
            for a in data['availability']:
                avail_id = a.get('id')

                if a.get('copy_time_from_montosun'):
                    DoctorAvailability.objects.filter(
                        doctor=doctor,
                        shift=a['shift']
                    ).delete()

                    for day, _ in DAY_CHOICES:
                        DoctorAvailability.objects.create(
                            doctor=doctor,
                            day=day,
                            shift=a['shift'],
                            from_time=a['from_time'],
                            to_time=a['to_time'],
                            copy_time_from_montosun=True,
                            updated_by=request.user
                        )

                elif avail_id:
                    DoctorAvailability.objects.filter(
                        id=avail_id,
                        doctor=doctor
                    ).update(
                        day=a['day'],
                        shift=a['shift'],
                        from_time=a['from_time'],
                        to_time=a['to_time'],
                        updated_by=request.user
                    )
                else:
                    DoctorAvailability.objects.create(
                        doctor=doctor,
                        **a,
                        updated_by=request.user
                    )

        # ----------- DOCUMENTS (ONLY IF SENT) -----------
        if 'documents' in data:
            for d in data['documents']:
                doc_id = d.get('id')

                if doc_id:
                    DoctorDocument.objects.filter(
                        id=doc_id,
                        doctor=doctor
                    ).update(
                        document_type_id=d['document_type'],
                        document_file=d.get('document_file'),
                        updated_by=request.user
                    )
                else:
                    DoctorDocument.objects.create(
                        doctor=doctor,
                        document_type_id=d['document_type'],
                        document_file=d['document_file'],
                        updated_by=request.user
                    )

        # ----------- BANK (ONLY IF SENT) -----------
        if 'bank' in data:
            DoctorBankDetail.objects.update_or_create(
                doctor=doctor,
                defaults={**data['bank'], 'updated_by': request.user}
            )

        return Response(
            self.get_serializer(doctor).data,
            status=status.HTTP_200_OK
        )
