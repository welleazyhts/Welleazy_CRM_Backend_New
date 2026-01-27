from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SecondOpinionCase
from .serializers import SecondOpinionCaseSerializer


class SecondOpinionCaseAPI(APIView):

    # 🔹 LIST ALL CASES
    def get(self, request):
        qs = SecondOpinionCase.objects.filter(is_active=True)
        serializer = SecondOpinionCaseSerializer(qs, many=True)
        return Response(serializer.data)

    # 🔹 CREATE CASE
    def post(self, request):
        serializer = SecondOpinionCaseSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                SecondOpinionCaseSerializer(obj).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
