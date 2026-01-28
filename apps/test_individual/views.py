from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import IndividualTest
from .serializers import IndividualTestSerializer
from rest_framework.permissions import IsAdminUser


class IndividualTestViewSet(ModelViewSet):
    queryset = IndividualTest.objects.all().order_by("-created_at")
    serializer_class = IndividualTestSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Extract health concern IDs (list)
        health_concern_ids = data.pop("health_concern_types", [])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        test = serializer.save(created_by=request.user)

        # Set many-to-many
        if health_concern_ids:
            test.health_concern_types.set(health_concern_ids)

        return Response(
            IndividualTestSerializer(test).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()

        health_concern_ids = data.pop("health_concern_types", None)

        serializer = self.get_serializer(
            instance,
            data=data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        test = serializer.save(updated_by=request.user)

        # Update many-to-many only if provided
        if health_concern_ids is not None:
            test.health_concern_type.set(health_concern_ids)

        return Response(IndividualTestSerializer(test).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Clear M2M before delete (good practice)
        instance.health_concern_type.clear()
        instance.delete()

        return Response(
            {"message": "Test deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# FLITERING THE INDIVIDUAL TEST LIST----


    def get_queryset(self):
        queryset = (
            IndividualTest.objects
            .select_related("client", "test_type", "visit_type")
            .prefetch_related("health_concern_type")
            .order_by("-created_at")
        )

        params = self.request.query_params

        sku_code = params.get("sku_code")
        test_name = params.get("test_name")
        test_code = params.get("test_code")
        corporate_name = params.get("corporate_name")
        status = params.get("status")

        if sku_code:
            queryset = queryset.filter(product_sku__icontains=sku_code)

        if test_name:
            queryset = queryset.filter(test_name__icontains=test_name)

        if test_code:
            queryset = queryset.filter(test_code__icontains=test_code)

        if corporate_name:
            queryset = queryset.filter(client__corporate_name__icontains=corporate_name)

        if status:
            queryset = queryset.filter(status=status)

        return queryset
