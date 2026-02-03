from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from .models import MiscellaneousProgramCase
from .serializers import (
    MiscellaneousProgramCaseSerializer, 
    MiscellaneousProgramCasePayloadSerializer
)
from .filters import MiscellaneousProgramCaseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class MiscellaneousProgramCaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MiscellaneousProgramCase.objects.select_related(
        'client', 'branch', 'employee', 'case_for', 
        'relationship_person', 'state', 'city', 'case_status',
        'created_by', 'updated_by'
    ).all().order_by('-created_at')
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MiscellaneousProgramCaseFilter
    search_fields = ['case_id', 'customer_name', 'mobile_no', 'email_id', 'care_program']
    ordering_fields = ['created_at', 'case_id']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MiscellaneousProgramCasePayloadSerializer
        return MiscellaneousProgramCaseSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        instance = serializer.instance
        return Response(
            {
                "message": "Miscellaneous Program Case created successfully",
                "data": MiscellaneousProgramCaseSerializer(instance).data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                "message": "Miscellaneous Program Case updated successfully",
                "data": MiscellaneousProgramCaseSerializer(instance).data
            },
            status=status.HTTP_200_OK
        )
