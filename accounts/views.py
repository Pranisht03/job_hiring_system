from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from applications.models import JobApplicant
from jobs.models import Job

# Home page
def home_view(request):
    return render(request, 'home.html')

# About page
def about_view(request):
    return render(request, 'about.html')

# Contact page
def contact_view(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, "accounts/login.html")

def choose_signup(request):
    return render(request, "accounts/signup.html")

def jobseeker_signup_page(request):
    return render(request, "accounts/signup_jobseeker.html")

def company_signup_page(request):
    return render(request, "accounts/signup_company.html")

@login_required
def jobseeker_dashboard(request):
    # Get all jobs applied by the logged-in user
    applied_jobs = JobApplicant.objects.filter(applicant=request.user)

    context = {
        'applied_jobs': applied_jobs,
    }
    return render(request, 'accounts/jobseeker_dashboard.html', context)

@login_required
def manage_applicants(request):
    if not request.user.is_company:
        # Optional: redirect if user is not a company
        return redirect('accounts:login')
    return render(request, "accounts/manage_applicants.html")

@login_required
def jobseeker_profile(request):
    if not request.user.is_job_seeker:
        return redirect('home')

    return render(request, 'accounts/jobseeker_profile.html')


@login_required
def manage_jobs(request):
    # Only allow company users
    if not request.user.is_company:
        messages.error(request, "Access denied. You are not a company user.")
        return redirect("home")  # or wherever suitable

    # Get jobs posted by this company
    jobs = Job.objects.filter(company=request.user).order_by('-created_at')

    # Search functionality
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(job_title__icontains=query)

    return render(request, "accounts/manage_jobs.html", {"jobs": jobs})

@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect('accounts:login')