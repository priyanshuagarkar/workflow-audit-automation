from rest_framework import serializers
from .models import WorkflowRequest

class WorkflowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowRequest
        fields = '__all__'
        read_only_fields = ("created_by","created_at")
