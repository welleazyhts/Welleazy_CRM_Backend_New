import json
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.core.choices import GENDER_CHOICES
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db import transaction
from django.db.models import Prefetch
from .models import LeadSource, LeadStatus, Lead, IndividualClient, IndividualClientDependent, IndividualClientDocument
from .serializers import (
    LeadSourceSerializer, LeadStatusSerializer, LeadSerializer, LeadPayloadSerializer,
    IndividualClientSerializer, IndividualClientPayloadSerializer
)
from .filters import LeadFilter, IndividualClientFilter
from apps.core.services import DocumentService


class LeadSourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = LeadSource.objects.select_related('created_by', 'updated_by').all().order_by('-created_at')
    serializer_class = LeadSourceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)
        return Response({
            "message": "Lead source created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response({
            "message": "Lead source updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Lead source deleted successfully"},
            status=status.HTTP_200_OK
        )


class LeadStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = LeadStatus.objects.select_related('created_by', 'updated_by').all().order_by('-created_at')
    serializer_class = LeadStatusSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)
        return Response({
            "message": "Lead status created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response({
            "message": "Lead status updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Lead status deleted successfully"},
            status=status.HTTP_200_OK
        )


class LeadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Lead.objects.select_related(
        'lead_source', 'lead_status', 'created_by', 'updated_by', 'state', 'city', 'policy_type', 'existing_insurer'
    ).all().order_by('-created_at')
    serializer_class = LeadSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LeadFilter
    search_fields = ['first_name', 'last_name', 'company_name', 'email', 'phone_no']
    ordering_fields = ['created_at', 'first_name', 'company_name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LeadPayloadSerializer
        return LeadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)
        return Response({
            "message": "Lead created successfully",
            "data": LeadSerializer(serializer.instance).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response({
            "message": "Lead updated successfully",
            "data": LeadSerializer(serializer.instance).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Lead deleted successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='completed')
    def completed_leads(self, request):
        completed_leads = self.get_queryset().filter(lead_status__name='Completed')
        serializer = self.get_serializer(completed_leads, many=True)
        return Response({
            "message": "Completed leads retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='choices')
    def get_choices(self, request):
        
        choices = {
            "lead_type": dict(Lead.LEAD_TYPE_CHOICES),
            "service_type": dict(Lead.SERVICE_TYPE_CHOICES),
            "service_category": dict(Lead.SERVICE_CATEGORY_CHOICES),
        }
        
        return Response({
            "message": "Lead choices retrieved successfully",
            "data": choices
        }, status=status.HTTP_200_OK)

from rest_framework.parsers import MultiPartParser, FormParser
class IndividualClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    queryset = IndividualClient.objects.select_related(
        'state', 'city', 'type_of_insurance', 'current_insurer', 'created_by', 'updated_by'
    ).prefetch_related(
        'documents',
        Prefetch(
            'dependents',
            queryset=IndividualClientDependent.objects.select_related('relationship')
        )
    ).all().order_by('-created_at')
    serializer_class = IndividualClientSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = IndividualClientFilter
    search_fields = [
        'employee_name', 'employee_id', 'contact_no', 
        'company_email', 'company_name'
    ]
    ordering_fields = ['created_at', 'employee_name', 'company_name', 'expiry_date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IndividualClientPayloadSerializer
        return IndividualClientSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.initial_data
        instance = serializer.save(created_by=self.request.user, updated_by=self.request.user)
        self._handle_related(instance, data)

    @transaction.atomic
    def perform_update(self, serializer):
        data = serializer.initial_data
        instance = serializer.save(updated_by=self.request.user)
        self._handle_related(instance, data)

    def _handle_related(self, instance, data):
        dependents_data = DocumentService.get_nested_data(data, 'dependents')
        documents_data = DocumentService.get_nested_data(data, 'documents')

        if dependents_data is not None:
            self._save_dependents(instance, dependents_data)

        if documents_data is not None or self.request.FILES:
            DocumentService.sync_documents(
                parent_instance=instance,
                files=self.request.FILES,
                documents_json=documents_data,
                model=IndividualClientDocument,
                parent_field='individual_client',
                file_field='document',
                user=self.request.user,
                include_keys=['documents', 'new_documents']
            )

    def _save_client_fields(self, client, validated):
        fields = [
            'employee_name', 'employee_id', 'contact_no', 'company_email',
            'company_name', 'company_address', 'state', 'city', 'gender',
            'date_of_birth', 'type_of_insurance', 'current_insurer',
            'expiry_date', 'premium_amount', 'sum_assured', 'status'
        ]
        for field in fields:
            if field in validated:
                setattr(client, field, validated[field])

    def _save_dependents(self, client, dependents_data):
        if dependents_data is None:
            return
        keep_ids = []

        from rest_framework.exceptions import ValidationError
        for data in dependents_data:
            dependent_id = data.get('id')
            
            clean_data = {}
            for k, v in data.items():
                if k in ['id', 'individual_client']:
                    continue
                if k == 'relationship' and isinstance(v, int):
                    clean_data['relationship_id'] = v
                else:
                    clean_data[k] = v

            if dependent_id:
                dependent = IndividualClientDependent.objects.filter(id=dependent_id, individual_client=client).first()
                if not dependent:
                    raise ValidationError({"dependents": f"Invalid dependent ID {dependent_id} for this client"})
                
                for attr, value in clean_data.items():
                    setattr(dependent, attr, value)
                dependent.updated_by = client.updated_by
                dependent.save()
                keep_ids.append(dependent.id)
            else:
                dependent = IndividualClientDependent.objects.create(
                    individual_client=client,
                    created_by=client.created_by,
                    updated_by=client.updated_by,
                    **clean_data
                )
                keep_ids.append(dependent.id)

        IndividualClientDependent.objects.filter(individual_client=client).exclude(id__in=keep_ids).delete()


    @action(detail=False, methods=['get'], url_path='choices')
    def get_choices(self, request):
        from apps.master_management.models import (
            State, City, MasterTypeOfInsurance, 
            MasterInsuranceCompany, MasterRelationship
        )
        
        choices = {
            "status": ["Active", "Inactive"],
            "gender": [{"id": g[0], "name": g[1]} for g in GENDER_CHOICES],
            "states": [{"id": s.id, "name": s.name} for s in State.objects.filter(is_active=True)],
            "insurance_types": [{"id": it.id, "name": it.name} for it in MasterTypeOfInsurance.objects.filter(is_active=True)],
            "insurance_companies": [{"id": ic.id, "name": ic.name, "type_of_insurance": ic.type_of_insurance_id} for ic in MasterInsuranceCompany.objects.filter(is_active=True)],
            "relationships": [{"id": r.id, "name": r.name} for r in MasterRelationship.objects.filter(is_active=True)],
        }
        
        return Response({
            "message": "Individual client choices retrieved successfully",
            "data": choices
        }, status=status.HTTP_200_OK)
