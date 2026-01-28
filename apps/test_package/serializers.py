from rest_framework import serializers
from .models import TestPackage
from apps.test_individual.models import IndividualTest


class TestPackageSerializer(serializers.ModelSerializer):

    client_name = serializers.CharField(source="client.corporate_name", read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)
    visit_type_name = serializers.CharField(source="visit_type.name", read_only=True)
    checkup_type_name = serializers.CharField(source="checkup_type.name", read_only=True)
    plancategory_name= serializers.CharField(source="plancategory.name" , read_only=True)
    gender_name=serializers.CharField(source="gender.name" , read_only=True)


    test_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TestPackage
        fields = "__all__"
        read_only_fields = (
            "product_sku",
            "created_at",
        )

    def get_test_names(self, obj):
        return [t.test_name for t in obj.tests_included.all()]
