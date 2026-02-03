from rest_framework import serializers
from .models import GymPackage , PlanCategory , PackagePriceType


# SERIALIZERS FOR THE DROPDOWNS-----

class PackagePriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagePriceType
        fields = "__all__"


# SERIALIZERS FOR MAIN TABLE-----


class GymPackageSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    plan_category_name=serializers.CharField(source="plan_category.name", read_only=True)
    package_price_name=serializers.CharField(source="package_price.name", read_only=True)
    gym_sku = serializers.ReadOnlyField()
    discount_package_price = serializers.ReadOnlyField()

    class Meta:
        model = GymPackage
        fields = '__all__'