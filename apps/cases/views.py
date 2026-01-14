from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Case
from .serializers import CaseSerializer

class CaseViewSet(ModelViewSet):
    queryset = Case.objects.all().order_by("-created_at")
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context