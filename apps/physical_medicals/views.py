from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import (
    PhysicalMedicalCase,
    PhysicalMedicalClientDetail,
    PhysicalMedicalCustomerDetail,
    PhysicalMedicalCaseDetail,
    PhysicalMedicalDependent
)

from .serializers import (
    PhysicalMedicalCaseSerializer,
    PhysicalMedicalCaseListSerializer
)


class PhysicalMedicalCaseViewSet(viewsets.ModelViewSet):
    queryset = PhysicalMedicalCase.objects.all()
    serializer_class = PhysicalMedicalCaseSerializer
    lookup_field = "case_id"

    # ========================
    # LIST
    # ========================
    def list(self, request):
        qs = self.get_queryset().order_by("-id")
        serializer = PhysicalMedicalCaseListSerializer(qs, many=True)
        return Response(serializer.data)

    # ========================
    # RETRIEVE
    # ========================
    def retrieve(self, request, case_id=None):
        case = get_object_or_404(PhysicalMedicalCase, case_id=case_id)
        serializer = PhysicalMedicalCaseSerializer(case)
        return Response(serializer.data)

    # ========================
    # CREATE / UPDATE (UPSERT)
    # ========================
    @transaction.atomic
    def create(self, request):
        data = request.data

        # -------- 1️⃣ CASE (MAIN) --------
        case, _ = PhysicalMedicalCase.objects.update_or_create(
            case_id=data.get("case_id"),
            defaults={
                "case_received_mode_id": data.get("case_received_mode"),
                "case_received_datetime": data.get(
                    "case_received_datetime", timezone.now()
                ),
                "case_status_id": data.get("case_status"),
            }
        )

        # -------- 2️⃣ CLIENT DETAIL --------
        client = data.get("client_detail", {})
        PhysicalMedicalClientDetail.objects.update_or_create(
            case=case,
            defaults={
                "client_id": client.get("client"),
                "client_branch_id": client.get("client_branch"),
                "customer_type_id": client.get("customer_type"),
                "product_id": client.get("product"),
                "service_offered_id": client.get("service_offered"),
                "received_by_name": client.get("received_by_name"),
                "received_mobile": client.get("received_mobile"),
                "received_email": client.get("received_email"),
                "department": client.get("department"),
            }
        )

        # -------- 3️⃣ CUSTOMER DETAIL (REQUIRED) --------
        customer = data.get("customer_detail")
        if not customer:
            return Response(
                {"error": "customer_detail is REQUIRED"},
                status=status.HTTP_400_BAD_REQUEST
            )

        PhysicalMedicalCustomerDetail.objects.update_or_create(
            case=case,
            defaults={
                "customer_name": customer.get("customer_name"),
                "mobile_number": customer.get("mobile_number"),
                "alternate_number": customer.get("alternate_number"),
                "gender_id": customer.get("gender"),
                "email_id": customer.get("email_id"),
                "state_id": customer.get("state"),
                "city_id": customer.get("city"),
                "pincode": customer.get("pincode"),
                "address": customer.get("address"),
                "area_locality": customer.get("area_locality"),
                "landmark": customer.get("landmark"),
                "date_of_birth": customer.get("date_of_birth"),
                "geo_location": customer.get("geo_location"),
            }
        )

        # -------- 4️⃣ CASE DETAIL --------
        case_detail = data.get("case_detail", {})

        PhysicalMedicalCaseDetail.objects.update_or_create(
            case=case,
            defaults={
                "medical_test_id": case_detail.get("medical_test"),
                "generic_test_id": case_detail.get("generic_test"),
                "customer_profile_id": case_detail.get("customer_profile"),
                "application_no": case_detail.get("application_no"),
                "case_type_id": case_detail.get("case_type"),
                "payment_type_id": case_detail.get("payment_type"),
                "case_for_id": case_detail.get("case_for"),
                "dhoc_payment_id": case_detail.get("dhoc_payment"),
                "customer_pay_amount": case_detail.get("customer_pay_amount"),
                "preferred_visit_type_id": case_detail.get("preferred_visit_type"),
                "preferred_appointment_datetime": case_detail.get(
                    "preferred_appointment_datetime"
                ),
                "company_name": case_detail.get("company_name"),
            }
        )

        # -------- 5️⃣ DEPENDENTS (ADD CASE LIST) --------
        dependents = data.get("dependents", [])

        # remove old dependents (important for update)
        PhysicalMedicalDependent.objects.filter(case=case).delete()

        for dep in dependents:
            PhysicalMedicalDependent.objects.create(
                case=case,
                case_for_id=dep.get("case_for"),
                dependent_name=dep.get("dependent_name"),
                mobile_number=dep.get("mobile_number"),
                gender_id=dep.get("gender"),
                date_of_birth=dep.get("date_of_birth"),
                address=dep.get("address"),
                medical_test_id=dep.get("medical_test"),
            )

        return Response(
            PhysicalMedicalCaseSerializer(case).data,
            status=status.HTTP_201_CREATED
        )

    # ========================
    # DELETE
    # ========================
    def destroy(self, request, case_id=None):
        case = get_object_or_404(PhysicalMedicalCase, case_id=case_id)
        case.delete()
        return Response(
            {"message": "Case deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
