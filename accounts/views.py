from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # <-- Missing import
from .serializers import RegisterSerializer  # <-- Missing import


class RegisterAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
