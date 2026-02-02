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
def jobseeker_profile(request):
    if not request.user.is_job_seeker:
        return redirect('home')

    return render(request, 'accounts/jobseeker_profile.html')


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect('accounts:login')