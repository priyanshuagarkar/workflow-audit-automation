from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WorkflowRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    APPROVAL_LEVELS = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    current_level = models.IntegerField(choices=APPROVAL_LEVELS, default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AuditLog(models.Model):
    workflow = models.ForeignKey(WorkflowRequest, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)