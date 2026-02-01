from django.contrib import admin
from .models import WorkflowRequest, AuditLog

admin.site.register(WorkflowRequest)
admin.site.register(AuditLog)
