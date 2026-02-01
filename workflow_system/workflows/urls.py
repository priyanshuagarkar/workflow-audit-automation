from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, create_workflow, my_requests, pending_approvals

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="workflows/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("dashboard/", dashboard, name="dashboard"),
    path("workflows/create/", create_workflow, name="create_workflow"),
    path("workflows/mine/", my_requests, name="my_requests"),
    path("workflows/pending/", pending_approvals, name="pending_approvals")
]
