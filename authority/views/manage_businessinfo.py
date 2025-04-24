from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, UpdateView, DeleteView,ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Home.models import BusinessInfo

from authority.forms import BusinessInfoForm

# <<----------------- List, Add, Update, Delete BusinessInfo ---------------->>


class BusinessInfoListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = BusinessInfo
    form_class = BusinessInfoForm
    template_name = 'business_info/business_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['businessinfo'] = BusinessInfo.objects.first()
        context['title'] = 'Business Info List'
        return context



class UpdateBusinessInfoView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = BusinessInfo
    form_class = BusinessInfoForm
    template_name = 'business_info/add_update_business.html'
    success_url = reverse_lazy('authority:business_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Business Info"
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Business info updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AddBusinessInfoView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = BusinessInfo
    form_class = BusinessInfoForm
    template_name = 'business_info/add_update_business.html'
    success_url = reverse_lazy('authority:business_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Business Info"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Business Info Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class BusinessInfoDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        business_info = get_object_or_404(BusinessInfo, pk=pk)
        business_info.delete()
        messages.success(request, "Business Info deleted successfully.")
        return redirect('authority:business_list')
