from django.urls import path
from . import views

urlpatterns = [
    path('manage/applicants/', views.manage_applicants, name='manage-applicants'),
    path('application/<int:pk>/<str:status>/', views.update_application_status, name='update-application-status'),
]
