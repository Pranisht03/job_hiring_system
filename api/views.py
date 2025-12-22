from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSeekerRegisterSerializer, CompanyRegisterSerializer
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer
from accounts.models import CustomUser
from django.shortcuts import redirect

@api_view(['POST'])
def register_jobseeker(request):
    serializer = JobSeekerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Job Seeker registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_company(request):
    serializer = CompanyRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Company registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user_type = serializer.validated_data['user_type']

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Check user type
            if user_type == 'jobseeker' and not user.is_job_seeker:
                return Response({"error": "Not a Job Seeker account."}, status=status.HTTP_400_BAD_REQUEST)
            if user_type == 'company' and not user.is_company:
                return Response({"error": "Not a Company account."}, status=status.HTTP_400_BAD_REQUEST)

            # Login and maintain session
            login(request, user)

            # Return redirect URL based on user type
            if user_type == 'jobseeker':
                return Response({"message": "Login successful!", "redirect_url": "/jobseeker_dashboard/"}, status=200)
            else:
                return Response({"message": "Login successful!", "redirect_url": "/company_dashboard/"}, status=200)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
