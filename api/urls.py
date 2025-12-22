from django.urls import path
from . import views

urlpatterns = [
    path('register/jobseeker/', views.register_jobseeker, name='register-jobseeker'),
    path('register/company/', views.register_company, name='register-company'),
    path('login/', views.login_user, name='login-user'),
]
