from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import ConsultationCase, ConsultationCaseDocument, ConsultationDoctorDetails
from .serializers import (
    ConsultationCaseSerializer,
    ConsultationCasePayloadSerializer,
    ConsultationDoctorDetailsSerializer,
    ConsultationDoctorDetailsPayloadSerializer
)
from .filters import ConsultationCaseFilter
from apps.core.services import DocumentService
from apps.client_product_service.models import ClientProductService
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.master_management.models import MasterProductSubCategory
from apps.client.serializers import ClientSerializer
from apps.client_branch.serializers import ClientBranchSerializer
from apps.master_management.serializers import MasterProductSubCategorySerializer

class ConsultationCaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = ConsultationCase.objects.select_related(
        'consultation_type', 'service', 'specialities_test_list',
        'welleazy_branch', 'corporate_name',
        'branch_name', 'state', 'city',
        'preferred_language', 'case_status',
        'created_by', 'updated_by'
    ).prefetch_related(
        'doctor_details', 'dependents', 'documents'
    ).order_by('-created_at')

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConsultationCaseFilter
    search_fields = [
        'customer_name', 'customer_mobile', 'application_no', 
        'customer_email', 'case_id', 'employee_name'
    ]
    ordering_fields = ['created_at', 'payable_amount', 'case_receive_date', 'follow_up_date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConsultationCasePayloadSerializer
        return ConsultationCaseSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.initial_data  

        instance = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

        self._handle_related(instance, data)

    @transaction.atomic
    def perform_update(self, serializer):
        data = serializer.initial_data  

        instance = serializer.save(
            updated_by=self.request.user
        )

        self._handle_related(instance, data)

    def _handle_related(self, instance, data):
        dependents = DocumentService.get_nested_data(data, 'dependents')
        documents = DocumentService.get_nested_data(data, 'documents')

        if dependents is not None:
            self._save_dependents(instance, dependents)

        if documents is not None or self.request.FILES:
            DocumentService.sync_documents(
                parent_instance=instance,
                files=self.request.FILES,
                documents_json=documents,
                model=ConsultationCaseDocument,
                parent_field='case',
                file_field='document_file',
                name_field='document_name',
                user=self.request.user,
                include_keys=['documents', 'new_documents']
            )


    def _save_doctor_details(self, case, doctor_details_data):
        if doctor_details_data is None:
            return
        from .models import ConsultationDoctorDetails

        keep_ids = []

        for item in doctor_details_data:
            item_id = item.get('id')
            clean_data = {}

            for k, v in item.items():
                if k in ['id', 'case', 'doctor_name']:
                    continue
                if k == 'doctor' and isinstance(v, int):
                    clean_data['doctor_id'] = v
                else:
                    clean_data[k] = v

            if item_id:
                obj = ConsultationDoctorDetails.objects.filter(
                    id=item_id, case=case
                ).first()
                if not obj:
                    raise ValidationError({"doctor_details": f"Invalid ID {item_id}"})

                for field, value in clean_data.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                obj = ConsultationDoctorDetails.objects.create(
                    case=case, **clean_data
                )

            keep_ids.append(obj.id)

        ConsultationDoctorDetails.objects.filter(case=case).exclude(
            id__in=keep_ids
        ).delete()

    def _save_dependents(self, case, dependents_data):
        if dependents_data is None:
            return
        from .models import ConsultationCaseDependent

        keep_ids = []

        for item in dependents_data:
            dependent_id = item.get('id')
            clean_data = {}

            for k, v in item.items():
                if k in ['id', 'case', 'relationship_name', 'preferred_language_name']:
                    continue
                if k in ['relationship', 'preferred_language'] and isinstance(v, int):
                    clean_data[f"{k}_id"] = v
                else:
                    clean_data[k] = v

            if dependent_id:
                obj = ConsultationCaseDependent.objects.filter(
                    id=dependent_id, case=case
                ).first()
                if not obj:
                    raise ValidationError({"dependents": f"Invalid ID {dependent_id}"})

                for field, value in clean_data.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                obj = ConsultationCaseDependent.objects.create(
                    case=case, **clean_data
                )

            keep_ids.append(obj.id)

        ConsultationCaseDependent.objects.filter(case=case).exclude(
            id__in=keep_ids
        ).delete()

    @action(detail=False, methods=['get'], url_path='filter/clients')
    def get_filtered_clients(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        client_ids = ClientProductService.objects.filter(
            product_id=product_id, is_active=True
        ).values_list('client_id', flat=True)

        clients = Client.objects.filter(id__in=client_ids, is_active=True)
        return Response(ClientSerializer(clients, many=True).data)

    @action(detail=False, methods=['get'], url_path='filter/services')
    def get_filtered_services(self, request):
        product_id = request.query_params.get('product_id')
        client_id = request.query_params.get('client_id')

        if not product_id or not client_id:
            return Response({"error": "product_id and client_id required"}, status=400)

        cps = ClientProductService.objects.filter(
            product_id=product_id, client_id=client_id, is_active=True
        ).prefetch_related('services')

        service_ids = {s.id for c in cps for s in c.services.all()}
        services = MasterProductSubCategory.objects.filter(id__in=service_ids)

        return Response(MasterProductSubCategorySerializer(services, many=True).data)

    @action(detail=False, methods=['get'], url_path='filter/branches')
    def get_filtered_branches(self, request):
        product_id = request.query_params.get('product_id')
        client_id = request.query_params.get('client_id')

        if not product_id or not client_id:
            return Response({"error": "product_id and client_id required"}, status=400)

        branch_ids = ClientProductService.objects.filter(
            product_id=product_id,
            client_id=client_id,
            is_active=True,
            branch__isnull=False
        ).values_list('branch_id', flat=True)

        branches = ClientBranch.objects.filter(
            id__in=branch_ids, is_active=True
        )

        return Response(ClientBranchSerializer(branches, many=True).data)


class ConsultationDoctorDetailsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUser]
    
    queryset = ConsultationDoctorDetails.objects.select_related(
        'case', 'doctor', 'preferred_language', 'case_status'
    ).all().order_by('-created_at')
    
    serializer_class = ConsultationDoctorDetailsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['case', 'doctor', 'status', 'preferred_language', 'case_status']
    search_fields = ['doctor__doctor_name', 'case__case_id', 'case__customer_name']
    ordering_fields = ['created_at', 'appointment_date_time']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConsultationDoctorDetailsPayloadSerializer
        return ConsultationDoctorDetailsSerializer
    
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
    
    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
