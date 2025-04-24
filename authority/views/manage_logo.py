from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, UpdateView, DeleteView,ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Home.models import Logosettings

from authority.forms import LogosettingsForm


#<<----------------- List, Add, Update, Delete Logo---------------->>
class LogosettingsListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = Logosettings
    template_name = 'logo/logosettings_list.html'
    context_object_name = 'logosettings_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Logo Settings'
        return context


class LogosettingsCreateView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Logosettings
    form_class = LogosettingsForm
    template_name = 'logo/add_update_logosettings.html'
    success_url = reverse_lazy('authority:logo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Logo Settings'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Logo Settings Created Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong, please try again!')
        return super().form_invalid(form)


class LogosettingsUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Logosettings
    form_class = LogosettingsForm
    template_name = 'logo/add_update_logosettings.html'
    success_url = reverse_lazy('authority:logo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Logo Settings'
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Logo Settings Updated Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong, please try again!')
        return super().form_invalid(form)

class LogosettingsDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        logo_settings = get_object_or_404(Logosettings, pk=pk)
        logo_settings.delete()
        messages.success(request, "Logo deleted successfully.")
        return redirect('authority:logo_list')