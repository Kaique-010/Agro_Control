from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import BranchForm, EnterpriseForm
from .models import Branch, Enterprise

class EnterpriseListView(ListView):
    model = Enterprise
    template_name = "enterprise_list.html"
    context_object_name = 'enterprises'

class EnterpriseCreateView(CreateView):
    model = Enterprise
    template_name = "enterprise_form.html"
    form_class = EnterpriseForm
    success_url = reverse_lazy("enterprise_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EnterpriseUpdateView(UpdateView):
    model = Enterprise
    template_name = "enterprise_form.html"
    form_class = EnterpriseForm
    success_url = reverse_lazy("enterprise_list")

class EnterpriseDeleteView(DeleteView):
    model = Enterprise
    template_name = "enterprise_delete.html"
    success_url = reverse_lazy("enterprise_list")

class BranchListView(ListView):
    model = Branch
    template_name = "branch_list.html"
    context_object_name = 'branches'

class BranchCreateView(CreateView):
    model = Branch
    template_name = "branch_form.html"
    form_class = BranchForm
    success_url = reverse_lazy("branch_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BranchUpdateView(UpdateView):
    model = Branch
    template_name = "branch_form.html"
    form_class = BranchForm
    success_url = reverse_lazy("branch_list")

class BranchDeleteView(DeleteView):
    model = Branch
    template_name = "branch_delete.html"
    success_url = reverse_lazy("branch_list")
