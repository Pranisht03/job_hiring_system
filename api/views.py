from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import JobSeekerRegisterSerializer, CompanyRegisterSerializer, LoginSerializer, JobSeekerProfileSerializer, JobSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from accounts.models import JobSeekerProfile
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from jobs.models import Job


@api_view(['POST'])
@permission_classes([AllowAny])
def register_jobseeker(request):
    serializer = JobSeekerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Job Seeker registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_company(request):
    serializer = CompanyRegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Job Seeker registered successfully!"},
            status=status.HTTP_201_CREATED
        )

    print(serializer.errors) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user_type = serializer.validated_data['user_type']

        user = authenticate(username=email, password=password)

        if user is not None:
            # Check user type
            if user_type == 'jobseeker' and not user.is_job_seeker:
                return Response({"error": "Not a Job Seeker account."}, status=400)

            if user_type == 'company' and not user.is_company:
                return Response({"error": "Not a Company account."}, status=400)

            # Proper session login
            login(request, user)

            return Response(
                {
                    "message": "Login successful!",
                    "redirect_url": "/"
                },
                status=200
            )

        return Response({"error": "Invalid email or password."}, status=400)

    return Response(serializer.errors, status=400)


# GET jobseeker profile
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def get_jobseeker_profile(request):
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
        serializer = JobSeekerProfileSerializer(profile)
        return Response({"exists": True, "profile": serializer.data})
    except JobSeekerProfile.DoesNotExist:
        return Response({"exists": False})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def save_jobseeker_profile(request):
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
        serializer = JobSeekerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
    except JobSeekerProfile.DoesNotExist:
        serializer = JobSeekerProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"success": True, "profile": serializer.data})

    return Response(serializer.errors, status=400)



class PostJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # ================ COMPANY CHECK =================
        if not hasattr(user, 'is_company') or not user.is_company:
            return Response(
                {"error": "Only companies can post jobs"},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        job_id = data.get("job_id")

        # ================= EDIT MODE =================
        if job_id:
            job = get_object_or_404(Job, id=job_id, company=user)
            serializer = JobSerializer(job, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Job updated successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ================= CREATE MODE =================
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save(company=user)
            return Response(
                {"message": "Job posted successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)