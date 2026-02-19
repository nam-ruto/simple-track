from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('INTERVIEWED', 'Interviewed'),
        ('OFFER', 'Offer'),
        ('REJECTED', 'Rejected'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    applied_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.job_title} - {self.company}"

    def get_status_color(self):
        colors = {
            'APPLIED': 'primary',
            'INTERVIEWED': 'warning',
            'OFFER': 'success',
            'REJECTED': 'danger',
        }
        return colors.get(self.status, 'secondary')

    def get_priority_color(self):
        colors = {
            'LOW': 'secondary',
            'MEDIUM': 'info',
            'HIGH': 'danger',
        }
        return colors.get(self.priority, 'secondary')