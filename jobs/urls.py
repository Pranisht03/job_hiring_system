from django.urls import path
from . import views
from .views import job_list, apply_job
from .models import Job

app_name = "jobs"

urlpatterns = [
    path('', job_list, name='job-list'),
    path("post/", views.post_job, name="post-job"),
    path("apply/<int:job_id>/", apply_job, name="apply-job"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),
    path("manage/", views.manage_jobs, name="manage-jobs"),
    path("post/<int:job_id>/", views.post_job, name="edit-job"),
    path("manage/<int:job_id>/delete/", views.delete_job, name="delete-job"),
]
