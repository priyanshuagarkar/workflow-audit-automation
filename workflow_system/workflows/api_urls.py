from django.urls import path
from .views import CreateWorkflowAPIView, ApproveWorkflowAPIView

urlpatterns = [
    path("workflows/create/", CreateWorkflowAPIView.as_view()),
    path("workflows/approve/<int:workflow_id>/", ApproveWorkflowAPIView.as_view()),
]
