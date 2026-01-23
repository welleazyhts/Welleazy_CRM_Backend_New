from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    PhysicalMedicalCase,
    PhysicalMedicalClientDetail,
    PhysicalMedicalCustomerDetail,
    PhysicalMedicalCaseDetail
)
from .models import PhysicalMedicalCase
from .serializers import (
    PhysicalMedicalCaseSerializer,
    PhysicalMedicalClientDetailSerializer,
    PhysicalMedicalCustomerDetailSerializer,
    PhysicalMedicalCaseDetailSerializer
)

class PhysicalMedicalAddCaseAPI(APIView):

    def post(self, request):
        data = request.data

        # 1️⃣ Save / Get main case
        case, case_created = PhysicalMedicalCase.objects.get_or_create(
            case_id=data["case_id"],
            defaults={
                "case_entry_datetime": data["case_entry_datetime"],
                "case_received_mode": data["case_received_mode"],
                "case_received_datetime": data["case_received_datetime"],
                "welleazy_branch": data["welleazy_branch"],
                "assigned_executive": data["assigned_executive"],
            }
        )

        # 2️⃣ Save / Get client details
        PhysicalMedicalClientDetail.objects.get_or_create(
            case=case,
            defaults={
                "client_name": data["client_name"],
                "branch_zone": data.get("branch_zone"),
                "branch_name": data["branch_name"],
                "customer_type": data["customer_type"],
                "product_name": data["product_name"],
                "services_offered": data["services_offered"],
                "received_by": data.get("received_by"),
                "mobile_number": data.get("client_mobile"),
                "email_id": data.get("client_email"),
                "department": data.get("department"),
            }
        )

        # 3️⃣ Save / Get customer details
        PhysicalMedicalCustomerDetail.objects.get_or_create(
            case=case,
            defaults={
                "customer_id": data["customer_id"],
                "customer_name": data["customer_name"],
                "mobile_number": data["customer_mobile"],
                "alternate_number": data.get("alternate_number"),
                "gender": data["gender"],
                "email_id": data["customer_email"],
                "state": data["state"],
                "city": data["city"],
                "pincode": data.get("pincode"),
                "address": data["address"],
                "area": data["area"],
                "landmark": data["landmark"],
                "date_of_birth": data.get("dob"),
                "geo_location": data.get("geo_location"),
            }
        )
        PhysicalMedicalCaseDetail.objects.update_or_create(
    case=case,
    defaults={
        "medical_test": data["medical_test"],
        "generic_test": data.get("generic_test"),
        "customer_profile": data["customer_profile"],
        "customer_pay_amount": data.get("customer_pay_amount", 0),
        "application_no": data["application_no"],
        "case_type": data["case_type"],
        "payment_type": data["payment_type"],
        "case_for": data["case_for"],
        "dhoc_payment": data.get("dhoc_payment"),
        "preferred_visit_type": data.get("preferred_visit_type"),
        "preferred_appointment_datetime": data.get("appointment_datetime"),
        "company_name": data.get("company_name"),
        "case_status": data.get("case_status", "Fresh Case"),
        "follow_up_date": data.get("follow_up_date"),
        "remark": data.get("remark"),
    }
)

   


        return Response(
            {
                "message": "Physical Medical Case Saved Successfully",
                "case_id": case.case_id,
                "created": case_created
            },
            status=status.HTTP_201_CREATED if case_created else status.HTTP_200_OK
        )

class PhysicalMedicalGetCaseAPI(APIView):

    def get(self, request, case_id):
        try:
            case = PhysicalMedicalCase.objects.get(case_id=case_id)
        except PhysicalMedicalCase.DoesNotExist:
            return Response(
                {"error": "Case not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        response_data = {
            "case": PhysicalMedicalCaseSerializer(case).data,
            "client": PhysicalMedicalClientDetailSerializer(case.client_detail).data,
            "customer": PhysicalMedicalCustomerDetailSerializer(case.customer_detail).data,
            "case_detail": PhysicalMedicalCaseDetailSerializer(case.case_detail).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)