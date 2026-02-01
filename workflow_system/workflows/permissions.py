from rest_framework.permissions import BasePermission

class IsApprover(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.exists()
    
class CanApproveWorkflow(BasePermission):
    def has_permission(self, request, view):
        workflow = view.get_workflow()

        if workflow.status != "PENDING":
            return False

        required_group = f"Approver_Level_{workflow.current_level}"
        return request.user.groups.filter(name=required_group).exists()