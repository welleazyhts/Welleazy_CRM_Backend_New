from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import ClientBranch
from .serializers import ClientBranchSerializer
from .filters import ClientBranchFilter

class ClientBranchViewSet(viewsets.ModelViewSet):
    queryset = ClientBranch.objects.all().order_by('-created_at')
    serializer_class = ClientBranchSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['branch_name', 'spoc_name', 'mobile_no', 'email_id', 'client__corporate_name']
    filterset_class = ClientBranchFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Client Branch created successfully",
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
                "message": "Client Branch updated successfully",
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
            {"message": "Client Branch deleted successfully"},
            status=status.HTTP_200_OK
        )
