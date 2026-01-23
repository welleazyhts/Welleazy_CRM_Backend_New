from rest_framework import serializers
from .models import *


class BaseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]


class PartnershipTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = PartnershipType


class SpecialtyTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = SpecialtyType


class OwnershipTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = OwnershipType




class ServiceCategorySerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = ServiceCategory


class RadiologyTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = RadiologyType


class DiscountServiceSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = DiscountService


class VoucherDiscountTypeSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = VoucherDiscountType


class DCUniqueNameSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = DCUniqueName


class PaymentTermSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = PaymentTerm
