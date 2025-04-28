from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db.models import Sum,Count,Q,F
from django.core.paginator import Paginator

# class-based view classes
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin
from django.shortcuts import get_object_or_404, redirect

# Import Models
from Course.models import(
 SiteSettings
)



#Import Forms
from authority.forms import(

    SiteSettingsForm

)

class SiteSettingsListView(LoginRequiredMixin,AdminPassesTestMixin, ListView):
    model = SiteSettings
    template_name = 'sitesettings/sitesettings_list.html'
    context_object_name = 'sitesettings_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.objects.first()
        return context


class AddSiteSettingView(LoginRequiredMixin,AdminPassesTestMixin, CreateView):
    model = SiteSettings
    template_name = 'sitesettings/add_update_sitesettings.html'
    form_class = SiteSettingsForm
    success_url = reverse_lazy('authority:site_settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Site Setting"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Site Setting Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class UpdateSiteSettingView(LoginRequiredMixin,AdminPassesTestMixin, UpdateView):
    model = SiteSettings
    template_name = 'sitesettings/add_update_sitesettings.html'
    form_class = SiteSettingsForm
    success_url = reverse_lazy('authority:site_settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Site Setting"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Site Setting Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class SiteSettingDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        site_setting = get_object_or_404(SiteSettings, pk=pk)
        site_setting.delete()
        messages.success(request, "Site_setting deleted successfully.")
        return redirect('authority:site_settings')

