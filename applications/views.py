from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import JobApplicant
from django.contrib import messages

@login_required
def manage_applicants(request):
    user = request.user
    if not user.is_company:
        messages.error(request, "Access denied.")
        return redirect("home")

    # Filter by match score if provided
    match_filter = request.GET.get("match", "")
    applicants = JobApplicant.objects.filter(job__company=user).select_related('job', 'applicant')

    if match_filter:
        try:
            match_filter = int(match_filter)
            applicants = applicants.filter(match_score__gte=match_filter)
        except ValueError:
            pass

    return render(request, "accounts/manage_applicants.html", {
        "applicants": applicants,
        "match_filter": match_filter,
    })


@login_required
def update_application_status(request, pk, status):
    user = request.user
    if not user.is_company:
        messages.error(request, "Access denied.")
        return redirect("home")

    application = get_object_or_404(JobApplicant, pk=pk, job__company=user)

    if status not in ["accepted", "rejected"]:
        messages.error(request, "Invalid status")
        return redirect("jobs:manage-applicants")

    application.status = status
    application.save()
    messages.success(request, f"Application {status} successfully.")
    return redirect("accounts:manage_applicants")