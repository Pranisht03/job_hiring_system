from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.role == 'employer':
                return redirect('employer_dashboard')
            else:
                return redirect('jobseeker_dashboard')
        else:
            error = "Invalid username or password"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')



def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # log in user
            if user.role == 'employer':
                return redirect('employer_dashboard')
            else:
                return redirect('jobseeker_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})  # project-level templates

def employer_dashboard(request):
    return render(request, 'employer_dashboard.html')  # project-level template

def jobseeker_dashboard(request):
    return render(request, 'jobseeker_dashboard.html')  # project-level template