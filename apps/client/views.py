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

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] 
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def _extract_payload(self, request):
        if isinstance(request.data, dict) and "data" in request.data:
            try:
                return json.loads(request.data["data"])
            except json.JSONDecodeError:
                raise ValidationError({"error": "Invalid JSON format in 'data' field"})
        return request.data

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClientFilter
    search_fields = ['corporate_name', 'corporate_code', 'email_id', 'mobile_no']
    ordering_fields = ['created_at', 'corporate_name']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        payload = self._extract_payload(request)

        serializer = ClientPayloadSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        client = Client(
            created_by=request.user,
            updated_by=request.user,
        )

        self._save_client_fields(client, validated, request)
        client.save()

        self._save_spocs(client, validated)
        self._save_documents(client, validated, request)

        return Response(
            {
                "message": "Client created successfully",
                "data": ClientSerializer(client, context={'request': request}).data
            },
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        client = self.get_object()
        payload = self._extract_payload(request)

        serializer = ClientPayloadSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        client.updated_by = request.user
        self._save_client_fields(client, validated, request)
        client.save()

        self._save_spocs(client, validated)
        self._save_documents(client, validated, request)

        return Response(
            {
                "message": "Client updated successfully",
                "data": ClientSerializer(client, context={'request': request}).data
            },
            status=status.HTTP_200_OK
        )

    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Client deleted successfully"},
            status=status.HTTP_200_OK
        )

    # HELPER METHODS
    
    def _save_client_fields(self, client, validated, request):
        simple_fields = [
            'corporate_code', 'corporate_name', 'mobile_no', 'landline_no', 'email_id',
            'head_office_address', 'branch_office_addresses', 'referred_by',
            'sales_manager', 'broker', 'ops_spoc', 'service_charges', 'pan_no',
            'gst_no', 'home_visit_charges', 'account_id', 'channel_partner_id',
            'website_url', 'billing_email_address', 'is_active', 'total_sponsored',
            'total_non_sponsored', 'is_dependent_sponsored',
            'case_registration_mail_auto_triggered', 'separate_account',
            'agreement_date', 'expiry_date'
        ]
        
        for field in simple_fields:
            if field in validated:
                setattr(client, field, validated[field])
        
        fk_fields = {
            'business_type': 'BusinessType',
            'corporate_type': 'CorporateType',
            'source': 'Source',
            'welleazy_crm': 'WelleazyCRM',
            'visit_type': 'VisitType',
            'corporate_partnership_status': 'PartnershipStatus',
            'client_agreement_from': 'ClientAgreementFrom',
            'frequency_of_payment': 'PaymentFrequency',
        }
        
        for field, model_name in fk_fields.items():
            if field in validated:
                field_id = validated[field]
                if field_id is None:
                    setattr(client, field, None)
                else:
                    setattr(client, f"{field}_id", field_id)
        
        # Handle image upload
        if 'background_image' in request.FILES:
            client.background_image = request.FILES['background_image']
        
        if not client.pk:
            client.save()
        
        if 'members_sponsored' in validated:
            client.members_sponsored.set(validated['members_sponsored'])
    
    def _save_spocs(self, client, validated):
        if 'spocs' in validated:
            for spoc_data in validated['spocs']:
                ClientSPOC.objects.create(
                    client=client,
                    person_name=spoc_data.get('person_name'),
                    mobile_no=spoc_data.get('mobile_no'),
                    designation_id=spoc_data.get('designation'),
                    contact_no=spoc_data.get('contact_no'),
                    email_id=spoc_data.get('email_id'),
                    receive_email_for=spoc_data.get('receive_email_for'),
                    created_by=client.created_by,
                    updated_by=client.updated_by,
                )
    
    def _save_documents(self, client, validated, request):
        if "keep_documents" in validated:
            keep_ids = validated["keep_documents"]
            ClientDocument.objects.filter(client=client).exclude(id__in=keep_ids).delete()
        files = (
            request.FILES.getlist("documents") or 
            request.FILES.getlist("files") or 
            request.FILES.getlist("file") or
            request.FILES.getlist("upload_document")
        )
        
        for file in files:
            ClientDocument.objects.create(
                client=client,
                file=file,
                created_by=request.user,
                updated_by=request.user,
            )

    # DOCUMENT MANAGEMENT ENDPOINTS
    
    @action(detail=True, methods=["post"], url_path="documents", parser_classes=[MultiPartParser])
    def add_document(self, request, pk=None):
        client = self.get_object()
        
        files = request.FILES.getlist("documents") or request.FILES.getlist("files") or request.FILES.getlist("file")
        
        if not files:
            raise ValidationError({"documents": "At least one file is required"})
        
        created_documents = []
        for file in files:
            document = ClientDocument.objects.create(
                client=client,
                file=file,
                created_by=request.user,
                updated_by=request.user,
            )
            created_documents.append(document)
        
        return Response(
            {
                "message": f"{len(created_documents)} document(s) uploaded successfully",
                "data": ClientDocumentSerializer(created_documents, many=True, context={'request': request}).data
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
    
    @action(detail=False, methods=["get"], url_path="generate-code")
    def generate_code(self, request):
        last_client = Client.objects.filter(corporate_code__startswith="WEZY").order_by('corporate_code').last()
        
        if last_client and last_client.corporate_code:
            try:
                last_code = last_client.corporate_code
                number_part = int(last_code.replace("WEZY", ""))
                new_number = number_part + 1
            except ValueError:
                new_number = 1
        else:
            new_number = 1
        
        new_code = f"WEZY{new_number:05d}"
        
        return Response(
            {"corporate_code": new_code},
            status=status.HTTP_200_OK
        )
