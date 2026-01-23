from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    CaseReceivedMode,
    CaseType,
    PaymentType,
    CaseFor,
    PreferredVisitType,
    CaseStatus,
    BranchZone,
    CustomerType,
    ServiceOffered,
    Gender,
    MedicalTest,
    GenericTest,
    CustomerProfile,
    DhocPaymentOption,
)

from .serializers import (
    CaseReceivedModeSerializer,
    CaseTypeSerializer,
    PaymentTypeSerializer,
    CaseForSerializer,
    PreferredVisitTypeSerializer,
    CaseStatusSerializer,
    BranchZoneSerializer,
    CustomerTypeSerializer,
    ServiceOfferedSerializer,
    GenderSerializer,
    MedicalTestSerializer,
    GenericTestSerializer,
    CustomerProfileSerializer,
    DhocPaymentOptionSerializer,
)
class BaseDropdownAPI(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        qs = self.model.objects.filter(is_active=True)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # ✅ RETURN CREATED OBJECT
            return Response(
                self.serializer_class(instance).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CaseReceivedModeAPI(BaseDropdownAPI):
    model = CaseReceivedMode
    serializer_class = CaseReceivedModeSerializer


class CaseTypeAPI(BaseDropdownAPI):
    model = CaseType
    serializer_class = CaseTypeSerializer


class PaymentTypeAPI(BaseDropdownAPI):
    model = PaymentType
    serializer_class = PaymentTypeSerializer


class CaseForAPI(BaseDropdownAPI):
    model = CaseFor
    serializer_class = CaseForSerializer


class PreferredVisitTypeAPI(BaseDropdownAPI):
    model = PreferredVisitType
    serializer_class = PreferredVisitTypeSerializer


class CaseStatusAPI(BaseDropdownAPI):
    model = CaseStatus
    serializer_class = CaseStatusSerializer


class BranchZoneAPI(BaseDropdownAPI):
    model = BranchZone
    serializer_class = BranchZoneSerializer


class CustomerTypeAPI(BaseDropdownAPI):
    model = CustomerType
    serializer_class = CustomerTypeSerializer


class ServiceOfferedAPI(BaseDropdownAPI):
    model = ServiceOffered
    serializer_class = ServiceOfferedSerializer


class GenderAPI(BaseDropdownAPI):
    model = Gender
    serializer_class = GenderSerializer


class MedicalTestAPI(BaseDropdownAPI):
    model = MedicalTest
    serializer_class = MedicalTestSerializer


class GenericTestAPI(BaseDropdownAPI):
    model = GenericTest
    serializer_class = GenericTestSerializer


class CustomerProfileAPI(BaseDropdownAPI):
    model = CustomerProfile
    serializer_class = CustomerProfileSerializer


class DhocPaymentOptionAPI(BaseDropdownAPI):
    model = DhocPaymentOption
    serializer_class = DhocPaymentOptionSerializer
