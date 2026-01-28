from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ClientLogin, MasterSubPermission
from .serializers import ClientLoginSerializer, ClientUserContextSerializer
from apps.master_management.models import MasterPermission

class ClientLoginViewSet(viewsets.ModelViewSet):
    queryset = ClientLogin.objects.all().select_related('client', 'branch', 'employee', 'user').prefetch_related('permissions')
    serializer_class = ClientLoginSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_permissions(self):
        return super().get_permissions()

    def list_permissions(self, request):

        permissions = MasterPermission.objects.prefetch_related('sub_permissions').filter(is_active=True)
        data = []
        for perm in permissions:
            sub_perms = perm.sub_permissions.filter(is_active=True)
            if sub_perms.exists():
                data.append({
                    "id": perm.id,
                    "name": perm.name,
                    "sub_permissions": [
                        {"id": sub.id, "name": sub.name} for sub in sub_perms
                    ]
                })
        return Response(data)

class ClientUserContextView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            client_login = request.user.client_login
            serializer = ClientUserContextSerializer(client_login)
            return Response(serializer.data)
        except ClientLogin.DoesNotExist:
            return Response({"detail": "This user is not a Client User."}, status=status.HTTP_404_NOT_FOUND)
