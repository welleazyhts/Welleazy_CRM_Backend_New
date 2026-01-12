from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from apps.accounts.permissions import IsAdminUserJWT
from apps.location.models import City
from .models import DiagnosticCenter
from .serializers import DiagnosticCenterSerializer
from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from .models import (
    DiagnosticCenter,
    DiagnosticLocation,
    DiagnosticServices,
    DiagnosticLabCapabilities,
    DiagnosticStaff,
    DiagnosticAccreditation,
    DiagnosticBanking,
    DiagnosticAgreement,
)
from .serializers import DiagnosticCenterSerializer

class DiagnosticCenterViewSet(ModelViewSet):
    serializer_class = DiagnosticCenterSerializer
    permission_classes = [IsAdminUserJWT]
    queryset = DiagnosticCenter.objects.select_related(
        "location",
        "diagnosticservices",
        "diagnosticlabcapabilities",
        "staff",
        "diagnosticaccreditation",
        "diagnosticbanking",
        "agreement",
    )

    # ---------- HELPERS ----------

    def _validate_staff(self, staff):
        if staff.get("ambulance_available"):
            if staff.get("bls_ambulance_count", 0) == 0 and staff.get("acls_ambulance_count", 0) == 0:
                return Response(
                    {"staff": "Provide BLS or ACLS ambulance count"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            staff["bls_ambulance_count"] = 0
            staff["acls_ambulance_count"] = 0
        return None

    def _validate_agreement(self, agreement):
        if agreement.get("mou_signed") and not agreement.get("mou_signed_date"):
            return Response(
                {"agreement": "MOU signed date is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if agreement.get("mou_signed") is False:
            agreement["mou_signed_date"] = None
        return None

    def _create_nested(self, model, center, payload):
        return model.objects.create(
            center=center,
            created_by=self.request.user,
            updated_by=self.request.user,
            **payload
        )

    def _update_nested(self, instance, payload):
        for key, value in payload.items():
            setattr(instance, key, value)
        instance.updated_by = self.request.user
        instance.save()

    # ---------- CREATE ----------

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        location = data.pop("location")

        city_id = location.get("city")
        try:
            location["city"] = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response(
        {"location": "Invalid city id"},
        status=status.HTTP_400_BAD_REQUEST
    )
        services = data.pop("services")
        lab = data.pop("lab_capabilities")
        staff = data.pop("staff")
        accreditation = data.pop("accreditation")
        banking = data.pop("banking")
        agreement = data.pop("agreement")

        staff_error = self._validate_staff(staff)
        if staff_error:
            return staff_error

        agreement_error = self._validate_agreement(agreement)
        if agreement_error:
            return agreement_error

        center = DiagnosticCenter.objects.create(
            **data,
            created_by=request.user,
            updated_by=request.user
        )

        self._create_nested(DiagnosticLocation, center, location)
        self._create_nested(DiagnosticServices, center, services)
        self._create_nested(DiagnosticLabCapabilities, center, lab)
        self._create_nested(DiagnosticStaff, center, staff)
        self._create_nested(DiagnosticAccreditation, center, accreditation)
        self._create_nested(DiagnosticBanking, center, banking)
        self._create_nested(DiagnosticAgreement, center, agreement)

        serializer = self.get_serializer(center)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ---------- UPDATE ----------

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        # Update main center
        for field in [
            "name", "center_code", "unique_name", "token_id",
            "provider_type", "grade", "vendor", "is_active"
        ]:
            if field in data:
                setattr(instance, field, data[field])

        instance.updated_by = request.user
        instance.save()

        # Update nested
        if "location" in data:
            location = data["location"]

            if "city" in location:
                try:
                    location["city"] = City.objects.get(id=location["city"])
                except City.DoesNotExist:
                    return Response(
                {"location": "Invalid city id"},
                status=status.HTTP_400_BAD_REQUEST
            )

            self._update_nested(instance.location, location)

        if "services" in data:
            self._update_nested(instance.diagnosticservices, data["services"])

        if "lab_capabilities" in data:
            self._update_nested(instance.diagnosticlabcapabilities, data["lab_capabilities"])

        if "staff" in data:
            staff = data["staff"]
            staff_error = self._validate_staff(staff)
            if staff_error:
                return staff_error
            self._update_nested(instance.staff, staff)

        if "accreditation" in data:
            self._update_nested(instance.diagnosticaccreditation, data["accreditation"])

        if "banking" in data:
            self._update_nested(instance.diagnosticbanking, data["banking"])

        if "agreement" in data:
            agreement = data["agreement"]
            agreement_error = self._validate_agreement(agreement)
            if agreement_error:
                return agreement_error
            self._update_nested(instance.agreement, agreement)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
    

