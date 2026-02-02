from django.urls import path
from . import views 

app_name = "applications" 

urlpatterns = [
    path('manage/applicants/', views.manage_applicants, name='manage_applicants'),
    path('application/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),
]
