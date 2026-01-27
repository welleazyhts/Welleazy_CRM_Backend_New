from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import ClientCustomer
from .serializers import ClientCustomerSerializer
from .filters import ClientCustomerFilter

class ClientCustomerViewSet(viewsets.ModelViewSet):
    queryset = ClientCustomer.objects.all().order_by('-created_at')
    serializer_class = ClientCustomerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = ClientCustomerFilter
    search_fields = ['customer_name', 'member_id', 'email_id', 'mobile_no']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {   
                "message": "Client Customer created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Client Customer updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Client Customer deleted successfully"
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='generate-member-id')
    def generate_member_id(self, request):

        last_customer = ClientCustomer.objects.order_by('id').last()
        next_id = "EMP000001"
        
        if last_customer and last_customer.member_id.startswith('EMP'):
            try:
                last_numeric_id = int(last_customer.member_id.replace('EMP', ''))
                next_numeric_id = last_numeric_id + 1
                next_id = f"EMP{next_numeric_id:06d}"
            except ValueError:
                pass
        
        return Response({"member_id": next_id}, status=status.HTTP_200_OK)
