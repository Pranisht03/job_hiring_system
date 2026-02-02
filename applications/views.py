from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from accounts.models import CustomUser
from .models import JobApplicant
from jobs.utils.skill_matcher import cosine_similarity  # your existing function

@login_required
def manage_applicants(request):
    """
    Company dashboard: manage applicants
    """
    # Only applicants for jobs posted by this company
    applications = JobApplicant.objects.filter(
        job__company=request.user
    ).select_related("job", "applicant").order_by("-applied_at")

    # Filters
    status = request.GET.get("status")
    job_id = request.GET.get("job")
    top = request.GET.get("top")

    if status:
        applications = applications.filter(status=status)

    if job_id:
        try:
            job_id_int = int(job_id)
            applications = applications.filter(job_id=job_id_int)
        except ValueError:
            job_id_int = None
    else:
        job_id_int = None

    applicant_data = []

    for app in applications:
        # Extract skills lists for cosine_similarity
        # job.skills_required is comma-separated string
        job_skills = [s.strip() for s in app.job.skills_required.split(",")] if app.job.skills_required else []

        # cv_skills: you must decide where the applicant skills come from
        # If you don't store skills in model, just pass empty list for now
        cv_skills = []  # placeholder if not storing skills in user
        # If you are parsing CV or another field, fill cv_skills here

        score = cosine_similarity(job_skills, cv_skills)

        # Top applicants filter
        if top == "1" and score < 70:
            continue

        applicant_data.append({
            "app": app,
            "match_score": score,
        })

    # Jobs posted by this company (for dropdown)
    jobs = Job.objects.filter(company=request.user)

    return render(
        request,
        "accounts/manage_applicants.html",
        {
            "applicants": applicant_data,
            "jobs": jobs,
            "selected_status": status,
            "selected_job": job_id_int or "",
            "selected_top": top,
        }
    )


@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(
        JobApplicant,
        id=app_id,
        job__company=request.user
    )

    if status in ["accepted", "rejected"]:
        application.status = status
        application.save()

    return redirect("applications:manage_applicants")
