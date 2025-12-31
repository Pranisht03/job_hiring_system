from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.test import APIRequestFactory
from api.views import PostJobAPIView
from jobs.models import Job

def home(request):
    return render(request, 'base.html')

def post_job(request):
    return render(request, 'jobs/post_jobs.html')


@login_required
def post_job(request):
    if not request.user.is_company:
        messages.error(request, "You are not authorized to post jobs.")
        return redirect("home")

    if request.method == "POST":
        data = request.POST.copy()

        # Create DRF request internally
        factory = APIRequestFactory()
        api_request = factory.post(
            "/api/jobs/post/",
            data
        )
        api_request.user = request.user
        api_request.session = request.session

        response = PostJobAPIView.as_view()(api_request)

        if response.status_code == 201:
            messages.success(request, "Job posted successfully!")
            return redirect("accounts:company-dashboard")

        messages.error(request, response.data)

    return render(
        request,
        "jobs/post_jobs.html",
        {
            "company_name": request.user.username
        }
    )

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'jobs': jobs
    }
    return render(request, 'jobs.html', context)
