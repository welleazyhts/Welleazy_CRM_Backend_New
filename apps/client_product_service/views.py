from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import ClientProductService
from .serializers import ClientProductServiceSerializer
from .filters import ClientProductServiceFilter
from django.db import transaction
from .services import ClientProductServiceService

class ClientProductServiceViewSet(viewsets.ModelViewSet):
    queryset = ClientProductService.objects.select_related(
        'login_type', 'client', 'branch', 'product', 'created_by', 'updated_by'
    ).prefetch_related('services').all().order_by('-created_at')
    serializer_class = ClientProductServiceSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['client__corporate_name', 'branch__branch_name', 'product__name']
    filterset_class = ClientProductServiceFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = ClientProductServiceService.get_grouped_mappings(queryset)
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, dict):
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

        client_id = data.get('client')
        product_ids = data.get('product_ids', [])
        branch_ids = data.get('branch_ids', [])
        service_ids = data.get('service_ids', [])
        login_type_id = data.get('login_type')
        is_active = data.get('is_active', True)

        if not client_id or not product_ids:
            return Response({"error": "Client and at least one Product are required"}, status=status.HTTP_400_BAD_REQUEST)

        stats, instances = ClientProductServiceService.synchronize_mappings(
            user=request.user,
            client_id=client_id,
            branch_ids=branch_ids,
            product_ids=product_ids,
            service_ids=service_ids,
            login_type_id=login_type_id,
            is_active=is_active
        )

        if stats["added"] == 0 and stats["updated"] == 0 and stats["removed"] == 0 and stats["unchanged"] > 0:
            message = "The selected products and services are already assigned for this client and branch."
        else:
            message = f"Sync Complete: {stats['added']} added, {stats['updated']} updated, {stats['removed']} removed, {stats['unchanged']} unchanged."

        return Response({
            "message": message,
            "stats": stats,
            "data": ClientProductServiceSerializer(instances, many=True).data
        }, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data, error = ClientProductServiceService.prepare_update_data(instance, request.data)
        
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', True))
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        
        return Response({
            "message": "Client Product Service updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Client Product Service deleted successfully"},
            status=status.HTTP_200_OK
        )
