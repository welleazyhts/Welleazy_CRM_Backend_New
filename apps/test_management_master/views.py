from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser


# Create your views here.


class TestTypeViewSet(ModelViewSet):
    queryset = TestType.objects.all()
    serializer_class = TestTypeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)




class HealthConcernTypeViewSet(ModelViewSet):
    queryset = HealthConcernType.objects.all()
    serializer_class = HealthConcernTypeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class PlanCategoryViewSet(ModelViewSet):
    queryset = PlanCategory.objects.all()
    serializer_class = PlanCategorySerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CheckUpTypeViewSet(ModelViewSet):
    queryset = CheckUpType.objects.all()
    serializer_class = CheckUpTypeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
