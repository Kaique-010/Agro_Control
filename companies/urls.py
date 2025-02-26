from django.urls import path
from .views import (
    BranchCreateView, BranchListView, BranchUpdateView, BranchDeleteView,
    EnterpriseCreateView, EnterpriseListView, EnterpriseUpdateView, EnterpriseDeleteView
)

urlpatterns = [
    path("enterprises/", EnterpriseListView.as_view(), name="enterprise_list"),
    path("enterprise/new/", EnterpriseCreateView.as_view(), name="enterprise_create"),
    path("enterprise/<int:pk>/edit/", EnterpriseUpdateView.as_view(), name="enterprise_update"),
    path("enterprise/<int:pk>/delete/", EnterpriseDeleteView.as_view(), name="enterprise_delete"),

    path("branches/", BranchListView.as_view(), name="branches_list"),
    path("branch/new/", BranchCreateView.as_view(), name="branch_create"),
    path("branch/<int:pk>/edit/", BranchUpdateView.as_view(), name="branch_update"),
    path("branch/<int:pk>/delete/", BranchDeleteView.as_view(), name="branch_delete"),
]
