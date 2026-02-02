from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.test import APIRequestFactory
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta

from api.views import PostJobAPIView
from jobs.models import Job
from applications.models import JobApplicant

from jobs.utils.cv_text_extractor import extract_text_from_cv
from jobs.utils.skill_matcher import normalize_skills, extract_cv_skills, cosine_similarity
from jobs.utils.skill_matcher import analyze_skill_gap  


def home(request):
    return render(request, 'base.html')


@login_required
def post_job(request):
    if not request.user.is_company:
        messages.error(request, "You are not authorized to post jobs.")
        return redirect("home")

    if request.method == "POST":
        data = request.POST.copy()

        factory = APIRequestFactory()
        api_request = factory.post("/api/jobs/post/", data)
        api_request.user = request.user
        api_request.session = request.session

        response = PostJobAPIView.as_view()(api_request)

        if response.status_code == 201:
            messages.success(request, "Job posted successfully!")
            return redirect("accounts:company-dashboard")

        messages.error(request, response.data)

    return render(request, "jobs/post_jobs.html", {
        "company_name": request.user.username
    })


# =====================================================
# JOB LIST VIEW
# =====================================================
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')

    # -------- SEARCH & FILTER --------
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
        jobs = jobs.filter(created_at__gte=now() - timedelta(days=int(date)))

    # -------- DEFAULT VALUES --------
    for job in jobs:
        job.match_score = None
        job.match_label = None
        job.skills_list = normalize_skills(job.skills_required) if job.skills_required else []

    # -------- AI MATCHING (FIXED CV CALL) --------
    if request.user.is_authenticated and hasattr(request.user, 'jobseekerprofile'):
        profile = request.user.jobseekerprofile

        if profile.cv:
            cv_text = extract_text_from_cv(profile.cv)  

            if cv_text:
                for job in jobs:
                    job_skills = normalize_skills(job.skills_required)
                    cv_skills = extract_cv_skills(cv_text, job_skills)
                    score = cosine_similarity(job_skills, cv_skills)

                    job.match_score = score
                    job.match_label = (
                        "Very Good" if score >= 90 else
                        "Good" if score >= 70 else
                        "Low"
                    )

    # -------- MATCH FILTER --------
    match = request.GET.get('match')
    if match:
        jobs = [job for job in jobs if job.match_score and job.match_score >= int(match)]

    return render(request, "jobs.html", {"jobs": jobs})


# =====================================================
# APPLY JOB 
# =====================================================
@login_required
def apply_job(request, job_id):
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("jobs:job-list")

    job = get_object_or_404(Job, id=job_id, is_active=True)

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


# =====================================================
# JOB DETAIL (SKILL GAP ANALYSIS)
# =====================================================
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    analysis = None

    if hasattr(request.user, 'jobseekerprofile'):
        profile = request.user.jobseekerprofile

        if profile.cv:
            cv_text = extract_text_from_cv(profile.cv)

            if cv_text:
                analysis = analyze_skill_gap(
                    job.skills_required,
                    cv_text
                )

    return render(request, "jobs/job_detail.html", {
        "job": job,
        "analysis": analysis
    })
