from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Case
from .serializers import CaseSerializer


class CaseViewSet(ModelViewSet):
    queryset = Case.objects.all().order_by("-created_at")
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]

    # 🔹 When a new case is created
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # 🔹 When a case is updated
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
