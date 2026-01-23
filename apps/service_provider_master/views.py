from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import *




class PartnershipTypeViewSet(ModelViewSet):
    queryset = PartnershipType.objects.all()
    serializer_class = PartnershipTypeSerializer
    permission_classes = [IsAdminUser]


class SpecialtyTypeViewSet(ModelViewSet):
    queryset = SpecialtyType.objects.all()
    serializer_class = SpecialtyTypeSerializer
    permission_classes = [IsAdminUser]


class OwnershipTypeViewSet(ModelViewSet):
    queryset = OwnershipType.objects.all()
    serializer_class = OwnershipTypeSerializer
    permission_classes = [IsAdminUser]



class ServiceCategoryViewSet(ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAdminUser]


class RadiologyTypeViewSet(ModelViewSet):
    queryset = RadiologyType.objects.all()
    serializer_class = RadiologyTypeSerializer
    permission_classes = [IsAdminUser]


class DiscountServiceViewSet(ModelViewSet):
    queryset = DiscountService.objects.all()
    serializer_class = DiscountServiceSerializer
    permission_classes = [IsAdminUser]


class VoucherDiscountTypeViewSet(ModelViewSet):
    queryset = VoucherDiscountType.objects.all()
    serializer_class = VoucherDiscountTypeSerializer
    permission_classes = [IsAdminUser]


class DCUniqueNameViewSet(ModelViewSet):
    queryset = DCUniqueName.objects.all()
    serializer_class = DCUniqueNameSerializer
    permission_classes = [IsAdminUser]


class PaymentTermViewSet(ModelViewSet):
    queryset = PaymentTerm.objects.all()
    serializer_class = PaymentTermSerializer
    permission_classes = [IsAdminUser]
