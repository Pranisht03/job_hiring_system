from django.urls import path
from . import views
from .views import get_jobseeker_profile, save_jobseeker_profile


urlpatterns = [
    path('register/jobseeker/', views.register_jobseeker, name='register-jobseeker'),
    path('register/company/', views.register_company, name='register-company'),
    path('login/', views.login_user, name='login-user'),
    path('jobseeker/profile/', views.get_jobseeker_profile, name='get-jobseeker-profile'),
    path('jobseeker/profile/save/', views.save_jobseeker_profile, name='save-jobseeker-profile'),
]
