from django.db import models
from django.conf import settings

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    skills_required = models.TextField()
    experience_required = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    vacancies = models.PositiveIntegerField(default=1)
    last_date_to_apply = models.DateField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} - {self.company.username}"
