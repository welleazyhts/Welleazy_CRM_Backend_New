from rest_framework import serializers
from .models import IndividualTest
from apps.test_management_master.models import HealthConcernType
class IndividualTestSerializer(serializers.ModelSerializer):

    # Read-only display fields
    city_name = serializers.CharField(source="city.name", read_only=True)
    client_name = serializers.CharField(source="client.corporate_name", read_only=True)
    visit_type_name = serializers.CharField(source="visit_type.name", read_only=True)
    test_type_name = serializers.CharField(source="test_type.name", read_only=True)

    # Health concerns → READ ONLY
    health_concern_type_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IndividualTest
        fields = "__all__"
        read_only_fields = (
            "product_sku",
            "test_code",
            "created_at",
            "health_concern_types",  # 👈 IMPORTANT
        )

    def get_health_concern_type_names(self, obj):
        return [hc.name for hc in obj.health_concern_type.all()]
