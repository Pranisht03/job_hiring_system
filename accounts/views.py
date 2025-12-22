from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 

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
    return render(request, "jobseeker_dashboard.html")

@login_required
def company_dashboard(request):
    if not request.user.is_company:
        # Optional: redirect if user is not a company
        return redirect('accounts:login')
    return render(request, "company_dashboard.html")
