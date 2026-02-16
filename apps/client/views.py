import json
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Client, ClientDocument, ClientSPOC
from .serializers import ClientSerializer, ClientPayloadSerializer, ClientDocumentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ClientFilter
from apps.core.services import DocumentService

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] 
    queryset = Client.objects.select_related(
        'business_type', 'corporate_type', 'source', 'welleazy_crm',
        'visit_type', 'corporate_partnership_status', 'client_agreement_from',
        'frequency_of_payment', 'created_by', 'updated_by'
    ).prefetch_related(
        'spocs', 'documents', 'members_sponsored'
    ).all().order_by('-created_at')
    serializer_class = ClientSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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
        spocs_data = DocumentService.get_nested_data(data, 'spocs')
        documents_data = DocumentService.get_nested_data(data, 'documents')

        if spocs_data is not None:
            self._save_spocs(instance, spocs_data)

        if documents_data is not None or self.request.FILES:
            DocumentService.sync_documents(
                parent_instance=instance,
                files=self.request.FILES,
                documents_json=documents_data,
                model=ClientDocument,
                parent_field='client',
                file_field='file',
                user=self.request.user,
                include_keys=['documents', 'new_documents']
            )

    def _save_client_fields(self, client, validated, request):
        simple_fields = [
            'corporate_name', 'mobile_no', 'landline_no', 'email_id',
            'head_office_address', 'branch_office_address', 'referred_by',
            'sales_manager', 'broker', 'ops_spoc', 'service_charges', 'pan_no',
            'gst_no', 'home_visit_charges', 'account_id', 'channel_partner_id',
            'website_url', 'billing_email_address', 'is_active', 'total_sponsored',
            'total_non_sponsored', 'is_dependent_sponsored',
            'case_registration_mail_auto_triggered', 'separate_access',
            'agreement_date', 'expiry_date'
        ]
        
        for field in simple_fields:
            if field in validated:
                setattr(client, field, validated[field])
        
        fk_fields = [
            'business_type', 'corporate_type', 'source', 'welleazy_crm',
            'visit_type', 'corporate_partnership_status', 'client_agreement_from',
            'frequency_of_payment'
        ]
        
        for field in fk_fields:
            if field in validated:
                setattr(client, field, validated[field])
        
        if 'background_image' in request.FILES:
            client.background_image = request.FILES['background_image']
        
        if 'members_sponsored' in validated:
            client.members_sponsored.set(validated['members_sponsored'])
    
    def _save_spocs(self, client, spocs_data):
        if spocs_data is None:
            return  
        keep_ids = []

        for spoc_data in spocs_data:
            spoc_id = spoc_data.get("id")
            receive_email_for = spoc_data.pop("receive_email_for", [])
            
            clean_data = {}
            for k, v in spoc_data.items():
                if k in ['id', 'client']:
                    continue
                if k == 'designation' and isinstance(v, int):
                    clean_data['designation_id'] = v
                else:
                    clean_data[k] = v

            if spoc_id:
                spoc = ClientSPOC.objects.filter(
                    id=spoc_id,
                    client=client
                ).first()

                if not spoc:
                    raise ValidationError({
                        "spocs": f"Invalid SPOC id {spoc_id} for this client"
                    })

                for field, value in clean_data.items():
                    setattr(spoc, field, value)

                spoc.updated_by = client.updated_by
                spoc.save()
                keep_ids.append(spoc.id)

            else:
                spoc = ClientSPOC.objects.create(
                    client=client,
                    created_by=client.created_by,
                    updated_by=client.updated_by,
                    **clean_data
                )
                keep_ids.append(spoc.id)

            if receive_email_for is not None:
                spoc.receive_email_for.set(receive_email_for)

        ClientSPOC.objects.filter(
            client=client
        ).exclude(id__in=keep_ids).delete()

    


    
    @action(detail=True, methods=["post"], url_path="documents", parser_classes=[MultiPartParser])
    def add_document(self, request, pk=None):
        client = self.get_object()
        
        files = request.FILES.getlist("documents") or request.FILES.getlist("files") or request.FILES.getlist("file")
        
        if not files:
            raise ValidationError({"documents": "At least one file is required"})
        
        DocumentService.sync_documents(
            parent_instance=client,
            files=request.FILES,
            documents_json=None, 
            model=ClientDocument,
            parent_field='client',
            file_field='file',
            user=request.user,
            include_keys=['documents', 'new_documents']
        )
        

        return Response(
            {
                "message": "Document(s) uploaded successfully",
                "data": ClientDocumentSerializer(client.documents.all(), many=True, context={'request': request}).data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=["delete"], url_path="documents/delete")
    def delete_document(self, request, pk=None):
        client = self.get_object()
        
        doc_id = request.data.get('document_id') or request.query_params.get('document_id')
        if not doc_id:
            raise ValidationError({"document_id": "This field is required"})
        
        document = get_object_or_404(
            ClientDocument,
            id=doc_id,
            client=client,
            deleted_at__isnull=True
        )
        
        document.delete()
        
        return Response(
            {"message": "Document deleted successfully"},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=["delete"], url_path="spocs/delete")
    def delete_spoc(self, request, pk=None):
        client = self.get_object()
        
        spoc_id = request.data.get('spoc_id') or request.query_params.get('spoc_id')
        if not spoc_id:
            raise ValidationError({"spoc_id": "This field is required"})
        
        spoc = get_object_or_404(
            ClientSPOC,
            id=spoc_id,
            client=client
        )
        
        spoc.delete()
        
        return Response(
            {"message": "SPOC deleted successfully"},
            status=status.HTTP_200_OK
        )
    
