from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import SubClient, SubClientSPOC
from .serializers import SubClientSerializer
from .filters import SubClientFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

class SubClientViewSet(viewsets.ModelViewSet):
    queryset = SubClient.objects.all().order_by("-created_at")
    serializer_class = SubClientSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SubClientFilter
    search_fields = ['name', 'mobile_no', 'email_id', 'client__corporate_name']
    ordering_fields = ['created_at', 'name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Sub Client created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Sub Client updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user if self.request.user.is_authenticated else None)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Sub Client deleted successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["delete"], url_path="spocs/delete")
    def delete_spoc(self, request, pk=None):
        sub_client = self.get_object()
        
        spoc_id = request.data.get('spoc_id') or request.query_params.get('spoc_id')
        if not spoc_id:
            return Response({"spoc_id": "This field is required"}, status=400)
        
        try:
            spoc = sub_client.spocs.get(id=spoc_id)
            spoc.delete()
            return Response({"message": "SPOC deleted successfully"}, status=200)
        except SubClientSPOC.DoesNotExist:
            return Response({"error": "SPOC not found"}, status=404)
