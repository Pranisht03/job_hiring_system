from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Login page
    path("login/", views.login_view, name="login"),

    path('logout/', views.logout_view, name='logout'),

    # Choose account type page
    path("signup/", views.choose_signup, name="signup"),

    # Jobseeker signup page
    path("register/jobseeker/", views.jobseeker_signup_page, name="jobseeker_signup"),

    # Company signup page
    path("register/company/", views.company_signup_page, name="company_signup"),

    path("jobseeker_dashboard/", views.jobseeker_dashboard, name="jobseeker-dashboard"),
    path("manage/applicants/", views.manage_applicants, name="manage_applicants"),

    path('jobseeker/profile/', views.jobseeker_profile, name='jobseeker_profile'),
    path('manage/jobs/', views.manage_jobs, name='manage_jobs'),
]
