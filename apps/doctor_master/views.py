from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser



class EmpanelForViewSet(ModelViewSet):
    queryset = EmpanelFor.objects.all()
    serializer_class = EmpanelForSerializer
    permission_classes=[IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DoctorTypeViewSet(ModelViewSet):
    queryset = DoctorType.objects.all()
    serializer_class = DoctorTypeSerializer
    permission_classes=[IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MeetLocationViewSet(ModelViewSet):
    queryset = MeetLocation.objects.all()
    serializer_class = MeetLocationSerializer
    permission_classes=[IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



class DocumentTypeViewSet(ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes=[IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)