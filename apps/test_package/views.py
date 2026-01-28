from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from .models import TestPackage
from .serializers import TestPackageSerializer
from apps.test_individual.models import IndividualTest
from rest_framework.permissions import IsAdminUser


class TestPackageViewSet(ModelViewSet):
    serializer_class = TestPackageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        client = serializer.validated_data.get("client")
        tests = serializer.validated_data.get("tests_included", [])

        self._validate_tests_belong_to_client(client, tests)

        serializer.save(created_by=self.request.user )

    def perform_update(self, serializer):
        client = serializer.validated_data.get(
            "client",
            serializer.instance.client
        )
        tests = serializer.validated_data.get(
            "tests_included",
            serializer.instance.tests_included.all()
        )

        self._validate_tests_belong_to_client(client, tests)

        serializer.save( updated_by=self.request.user)

    def _validate_tests_belong_to_client(self, client, tests):
        invalid_tests = [
            test.test_name
            for test in tests
            if test.client_id != client.id
        ]

        if invalid_tests:
            raise ValidationError({
                "tests_included": (
                    "These tests do not belong to the selected client: "
                    + ", ".join(invalid_tests)
                )
            })
        

    def get_queryset(self):
        queryset = (
            TestPackage.objects
            .select_related("client", "checkup_type")
            .prefetch_related("tests_included")
            .order_by("-created_at")
        )

        params = self.request.query_params

        sku_code = params.get("sku_code")
        package_name = params.get("package_name")
        corporate_name = params.get("corporate_name")
        status = params.get("status")

        # 🔹 SKU Code filter
        if sku_code:
            queryset = queryset.filter(product_sku__icontains=sku_code)

        # 🔹 Package Name filter
        if package_name:
            queryset = queryset.filter(package_name__icontains=package_name)

        # 🔹 Corporate Name filter
        if corporate_name:
            queryset = queryset.filter(client__corporate_name__icontains=corporate_name)

        # 🔹 Status filter
        if status:
            queryset = queryset.filter(status=status)

        return queryset