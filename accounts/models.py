from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_job_seeker = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # comma-separated
    education = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.email
