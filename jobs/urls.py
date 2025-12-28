from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('', views.home, name='home'),
    path("post_job/", views.post_job, name="post_job"),
]
