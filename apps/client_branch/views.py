from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import ClientBranch
from .serializers import ClientBranchSerializer
from .filters import ClientBranchFilter

class ClientBranchViewSet(viewsets.ModelViewSet):
    queryset = ClientBranch.objects.select_related(
        'client', 'branch_zone', 'state', 'city', 'created_by', 'updated_by'
    ).all().order_by('-created_at')
    serializer_class = ClientBranchSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['branch_name', 'spoc_name', 'mobile_no', 'email_id', 'client__corporate_name']
    filterset_class = ClientBranchFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        branch = ClientBranch(
            created_by=request.user if request.user.is_authenticated else None,
            updated_by=request.user if request.user.is_authenticated else None,
        )

        self._save_branch_fields(branch, validated)
        branch.save()

        return Response(
            {
                "message": "Client Branch created successfully",
                "data": ClientBranchSerializer(branch).data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        branch = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        branch.updated_by = request.user if request.user.is_authenticated else None
        self._save_branch_fields(branch, validated)
        branch.save()

        return Response(
            {
                "message": "Client Branch updated successfully",
                "data": ClientBranchSerializer(branch).data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Client Branch deleted successfully"},
            status=status.HTTP_200_OK
        )

    # HELPER METHODS

    def _save_branch_fields(self, branch, validated):
        simple_fields = [   
            'branch_name', 'spoc_name', 'mobile_no', 'email_id',
            'address', 'is_active'
        ]
        
        for field in simple_fields:
            if field in validated:
                setattr(branch, field, validated[field])
        
        fk_fields = ['client', 'branch_zone', 'state', 'city']
        for field in fk_fields:
            if field in validated:
                setattr(branch, field, validated[field])
