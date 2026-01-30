from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from .serializers import CaseReceivedModeSerializer
from rest_framework.generics import ListCreateAPIView
from .models import CaseReceivedMode


# 🔹 Case Type
class SecondOpinionCaseTypeAPI(APIView):

    def get(self, request):
        qs = SecondOpinionCaseType.objects.filter(is_active=True)
        return Response(SecondOpinionCaseTypeSerializer(qs, many=True).data)

    def post(self, request):
        serializer = SecondOpinionCaseTypeSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                SecondOpinionCaseTypeSerializer(obj).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)


# 🔹 Interpretation Type
class InterpretationTypeAPI(APIView):

    def get(self, request):
        qs = InterpretationType.objects.filter(is_active=True)
        return Response(InterpretationTypeSerializer(qs, many=True).data)

    def post(self, request):
        serializer = InterpretationTypeSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                InterpretationTypeSerializer(obj).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)
class CaseReceivedModeAPI(ListCreateAPIView):
    queryset = CaseReceivedMode.objects.all()
    serializer_class = CaseReceivedModeSerializer