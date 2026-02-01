from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkflowRequest, AuditLog

@receiver(post_save, sender=WorkflowRequest)
def create_audit_log(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            workflow=instance,
            action="CREATED",
            performed_by=instance.created_by,
            remarks="Workflow created"
        )
