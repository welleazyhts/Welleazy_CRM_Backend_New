from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import ClientCustomer
from .serializers import ClientCustomerSerializer
from .filters import ClientCustomerFilter
from .services import ClientCustomerService

class ClientCustomerViewSet(viewsets.ModelViewSet):
    queryset = ClientCustomer.objects.all().order_by('-created_at')
    serializer_class = ClientCustomerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = ClientCustomerFilter
    search_fields = ['customer_name', 'member_id', 'email_id', 'mobile_no']

    def create(self, request, *args, **kwargs):
        service = ClientCustomerService()
        try:
            instance = service.upsert_customer(request.user, request.data)
            serializer = self.get_serializer(instance)
            return Response(
                {   
                    "message": "Client Customer created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        service = ClientCustomerService()
        try:
            # For partial updates, we might need more care with nested data
            # but currently upsert_customer handles what's passed in data.
            instance = service.upsert_customer(request.user, request.data, instance=instance)
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "message": "Client Customer updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
