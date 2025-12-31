from django.db import models
from django.conf import settings
from jobs.models import Job

User = settings.AUTH_USER_MODEL


class JobApplicant(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_applications")

    phone = models.CharField(max_length=15)
    cv = models.FileField(upload_to="cvs/")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant.email} → {self.job.job_title}"
