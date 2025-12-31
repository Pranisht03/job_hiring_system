from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
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

def jobseeker_dashboard(request):
    if not request.user.is_job_seeker:
        # Optional: redirect if user is not a jobseeker
        return redirect('accounts:login')
    return render(request, "accounts/jobseeker_dashboard.html")

@login_required
def company_dashboard(request):
    if not request.user.is_company:
        # Optional: redirect if user is not a company
        return redirect('accounts:login')
    return render(request, "accounts/company_dashboard.html")

@login_required
def jobseeker_profile(request):
    if not request.user.is_job_seeker:
        return redirect('home')

    return render(request, 'accounts/jobseeker_profile.html')


@login_required
def company_profile(request):
    if not request.user.is_company:
        return redirect('home')

    return render(request, 'accounts/company_profile.html')

@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect('accounts:login')
