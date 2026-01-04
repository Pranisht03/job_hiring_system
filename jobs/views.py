from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.test import APIRequestFactory
from api.views import PostJobAPIView
from jobs.models import Job
from django.shortcuts import get_object_or_404, redirect
from applications.models import JobApplicant
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta

from .utils.cv_text_extractor import extract_text_from_cv
from jobs.utils.skill_matcher import normalize_skills, extract_cv_skills, cosine_similarity

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
    jobs = Job.objects.all().order_by('-created_at')

    # ================= SEARCH & FILTER (DB LEVEL) =================

    q = request.GET.get('q')
    if q:
        jobs = jobs.filter(
            Q(job_title__icontains=q) |
            Q(company__company_name__icontains=q) |
            Q(skills_required__icontains=q)
        )

    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)

    date = request.GET.get('date')
    if date:
        jobs = jobs.filter(
            created_at__gte=now() - timedelta(days=int(date))
        )

    # ================= DEFAULT MATCH VALUES =================

    for job in jobs:
        job.match_score = None
        job.match_label = None

        if job.skills_required:
            job.skills_list = [s.strip() for s in job.skills_required.split(",")]
        else:
            job.skills_list = []

    # ================= AI MATCHING LOGIC =================

    if request.user.is_authenticated and hasattr(request.user, 'jobseekerprofile'):
        profile = request.user.jobseekerprofile

        if profile.cv:
            cv_text = extract_text_from_cv(profile.cv.path)

            for job in jobs:
                job_skills = normalize_skills(job.skills_required)
                cv_skills = extract_cv_skills(cv_text, job_skills)
                score = cosine_similarity(job_skills, cv_skills)

                job.match_score = score

                if score >= 90:
                    job.match_label = "Very Good"
                elif score >= 70:
                    job.match_label = "Good"
                else:
                    job.match_label = "Low"

    # ================= MATCH SCORE FILTER (POST AI) =================

    match = request.GET.get('match')
    if match:
        jobs = [job for job in jobs if job.match_score is not None and job.match_score >= int(match)]

    return render(request, "jobs.html", {"jobs": jobs})




@login_required
def apply_job(request, job_id):
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("jobs:job-list")

    job = get_object_or_404(Job, id=job_id, is_active=True)

    # Prevent duplicate application
    if JobApplicant.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("jobs:job-list")

    if request.method == "POST":
        phone = request.POST.get("phone")
        cv = request.FILES.get("cv")

        if not phone or not cv:
            messages.error(request, "All fields are required.")
            return redirect("jobs:job-list")

        JobApplicant.objects.create(
            job=job,
            applicant=request.user,
            phone=phone,
            cv=cv
        )

        messages.success(request, "Job applied successfully!")
        return redirect("jobs:job-list")

    messages.error(request, "Invalid request.")
    return redirect("jobs:job-list")