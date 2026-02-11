from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import ConsultationCase
from .serializers import ConsultationCaseSerializer, ConsultationCasePayloadSerializer
from apps.client_product_service.models import ClientProductService
from apps.client.models import Client
from apps.client.serializers import ClientSerializer
from apps.client_branch.models import ClientBranch
from apps.client_branch.serializers import ClientBranchSerializer
from apps.master_management.models import MasterProductSubCategory
from apps.master_management.serializers import MasterProductSubCategorySerializer

class ConsultationCaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ConsultationCase.objects.select_related(
        'consultation_type', 'service', 'specialities_test_list',
        'welleazy_branch', 'corporate_name',
        'branch_name', 'gender', 'state', 'city',
        'preferred_language', 'sponsor_status', 'case_status',
        'created_by', 'updated_by'
    ).prefetch_related('appointments').all().order_by('-created_at')
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['consultation_type', 'corporate_name', 'case_status', 'customer_type', 'payment_status']
    search_fields = ['customer_name', 'customer_mobile', 'application_no', 'customer_email']
    ordering_fields = ['created_at', 'payable_amount']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConsultationCasePayloadSerializer
        return ConsultationCaseSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        appointments_data = self.request.data.get('appointments', [])
        instance = serializer.save(created_by=self.request.user, updated_by=self.request.user)
        self._save_appointments(instance, appointments_data)

    @transaction.atomic
    def perform_update(self, serializer):
        appointments_data = self.request.data.get('appointments', [])
        instance = serializer.save(updated_by=self.request.user)
        if 'appointments' in self.request.data:
            self._save_appointments(instance, appointments_data)

    def _save_appointments(self, case, appointments_data):
        from .models import ConsultationAppointment
        keep_ids = []
        for item in appointments_data:
            appointment_id = item.get('id')
            if appointment_id:
                # Update existing
                appointment = ConsultationAppointment.objects.filter(id=appointment_id, case=case).first()
                if appointment:
                    for field, value in item.items():
                        if field not in ['id', 'case']:
                            setattr(appointment, field, value)
                    appointment.save()
                    keep_ids.append(appointment.id)
            else:
                # Create new
                appointment = ConsultationAppointment.objects.create(
                    case=case,
                    **{k: v for k, v in item.items() if k not in ['id', 'case']}
                )
                keep_ids.append(appointment.id)
        
        # Delete removed
        ConsultationAppointment.objects.filter(case=case).exclude(id__in=keep_ids).delete()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        instance = serializer.instance
        return Response(
            {
                "message": "Consultation Case created successfully",
                "data": ConsultationCaseSerializer(instance).data
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
                "message": "Consultation Case updated successfully",
                "data": ConsultationCaseSerializer(instance).data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Consultation Case deleted successfully"},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='choices')
    def get_choices(self, request):

        choices = {
            "case_rec_mode": dict(ConsultationCase.CASE_REC_MODE_CHOICES),
            "customer_type": dict(ConsultationCase.CUSTOMER_TYPE_CHOICES),
            "case_for": dict(ConsultationCase.CASE_FOR_CHOICES),
            "customer_profile": dict(ConsultationCase.CUSTOMER_PROFILE_CHOICES),
            "payment_type": dict(ConsultationCase.PAYMENT_TYPE_CHOICES),
            "payment_mode": dict(ConsultationCase.PAYMENT_MODE_CHOICES),
            "paying_to": dict(ConsultationCase.PAYING_TO_CHOICES),
            "payment_status": dict(ConsultationCase.PAYMENT_STATUS_CHOICES),
            "appointment_status": dict(ConsultationCase.APPOINTMENT_STATUS_CHOICES),
        }
        
        return Response({
            "message": "Consultation choices retrieved successfully",
            "data": choices
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='filter/clients')
    def get_filtered_clients(self, request):
        
        product_id = request.query_params.get('product_id')
        
        if not product_id:
            return Response(
                {"error": "product_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all clients that have this product mapped
        client_ids = ClientProductService.objects.filter(
            product_id=product_id,
            is_active=True
        ).values_list('client_id', flat=True).distinct()
        
        clients = Client.objects.filter(
            id__in=client_ids,
            is_active=True
        ).select_related('business_type', 'corporate_type')
        
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        
        return Response({
            "message": f"Found {clients.count()} client(s) with product_id={product_id}",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='filter/services')
    def get_filtered_services(self, request):
        
        product_id = request.query_params.get('product_id')
        client_id = request.query_params.get('client_id')
        
        if not product_id or not client_id:
            return Response(
                {"error": "Both product_id and client_id query parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all services mapped to this product for this client
        client_product_services = ClientProductService.objects.filter(
            product_id=product_id,
            client_id=client_id,
            is_active=True
        ).prefetch_related('services')
        
        # Collect all unique services
        service_ids = set()
        for cps in client_product_services:
            service_ids.update(cps.services.values_list('id', flat=True))
        
        services = MasterProductSubCategory.objects.filter(id__in=service_ids)
        
        serializer = MasterProductSubCategorySerializer(services, many=True)
        
        return Response({
            "message": f"Found {services.count()} service(s) for product_id={product_id} and client_id={client_id}",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='filter/branches')
    def get_filtered_branches(self, request):
        
        product_id = request.query_params.get('product_id')
        client_id = request.query_params.get('client_id')
        
        if not product_id or not client_id:
            return Response(
                {"error": "Both product_id and client_id query parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all branches that have this product mapped for this client
        branch_ids = ClientProductService.objects.filter(
            product_id=product_id,
            client_id=client_id,
            is_active=True,
            branch__isnull=False
        ).values_list('branch_id', flat=True).distinct()
        
        branches = ClientBranch.objects.filter(
            id__in=branch_ids,
            client_id=client_id,
            is_active=True
        ).select_related('client', 'branch_zone', 'state', 'city')
        
        serializer = ClientBranchSerializer(branches, many=True, context={'request': request})
        
        return Response({
            "message": f"Found {branches.count()} branch(es) for product_id={product_id} and client_id={client_id}",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
