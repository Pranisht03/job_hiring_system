from django.urls import path
from . import views
from .views import job_list

app_name = "jobs"

urlpatterns = [
    path('', job_list, name='jobs'),
    path("post/", views.post_job, name="post-job"),
]
