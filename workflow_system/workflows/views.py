from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import WorkflowRequest, AuditLog
from .serializers import WorkflowRequestSerializer
from .tasks import send_workflow_notification
from .permissions import CanApproveWorkflow
# Create your views here.

class CreateWorkflowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WorkflowRequestSerializer(data=request.data)
        if serializer.is_valid():
            workflow = serializer.save(created_by=request.user)

            send_workflow_notification.delay(workflow.id)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class ApproveWorkflowAPIView(APIView):
    permission_classes = [IsAuthenticated, CanApproveWorkflow]

    def get_workflow(self):
        return get_object_or_404(
            WorkflowRequest,
            id=self.kwargs["workflow_id"]
        )

    def post(self, request, workflow_id):
        workflow = self.get_workflow()

        action = request.data.get("action")

        if action == "REJECT":
            workflow.status = "REJECTED"
            workflow.save()

            AuditLog.objects.create(
                workflow=workflow,
                action="REJECTED",
                performed_by=request.user,
                remarks=f"Rejected at level {workflow.current_level}"
            )

            return Response({"message": "Workflow rejected"})

        # APPROVE flow
        if workflow.current_level < 3:
            workflow.current_level += 1
        else:
            workflow.status = "APPROVED"

        workflow.save()

        AuditLog.objects.create(
            workflow=workflow,
            action="APPROVED",
            performed_by=request.user,
            remarks=f"Approved at level {workflow.current_level}"
        )

        return Response({"message": "Workflow updated"})
    
@login_required
def dashboard(request):
    user_groups = request.user.groups.values_list("name", flat=True)

    level = None
    if "Approver_Level_1" in user_groups:
        level = 1
    elif "Approver_Level_2" in user_groups:
        level = 2
    elif "Approver_Level_3" in user_groups:
        level = 3

    my_requests_count = WorkflowRequest.objects.filter(
        created_by=request.user
    ).count()

    pending_approvals_count = 0
    if level:
        pending_approvals_count = WorkflowRequest.objects.filter(
            status="PENDING",
            current_level=level
        ).count()

    return render(
        request,
        "workflows/dashboard.html",
        {
            "my_requests_count": my_requests_count,
            "pending_approvals_count": pending_approvals_count
        }
    )


@login_required
def create_workflow(request):
    if request.method == "POST":
        WorkflowRequest.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            created_by=request.user
        )
        return redirect("dashboard")
    return render(request, "workflows/create.html")

@login_required
def my_requests(request):
    workflows = WorkflowRequest.objects.filter(created_by=request.user)
    return render(request, "workflows/my_requests.html", {"workflows": workflows})

@login_required
def pending_approvals(request):
    user_groups = request.user.groups.values_list("name", flat=True)

    # Determine which level this user can approve
    level = None
    if "Approver_Level_1" in user_groups:
        level = 1
    elif "Approver_Level_2" in user_groups:
        level = 2
    elif "Approver_Level_3" in user_groups:
        level = 3

    workflows = WorkflowRequest.objects.none()

    if level:
        workflows = WorkflowRequest.objects.filter(
            status="PENDING",
            current_level=level
        )

    return render(
        request,
        "workflows/pending.html",
        {"workflows": workflows}
    )


