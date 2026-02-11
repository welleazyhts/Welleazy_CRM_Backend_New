from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import LeadSource, LeadStatus, Lead
from .serializers import LeadSourceSerializer, LeadStatusSerializer, LeadSerializer, LeadPayloadSerializer
from .filters import LeadFilter


class LeadSourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = LeadSource.objects.all().order_by('-created_at')
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
    queryset = LeadStatus.objects.all().order_by('-created_at')
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
        'lead_source', 'lead_status', 'gender', 'created_by', 'updated_by'
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
