from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404, redirect
from django.forms import inlineformset_factory

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Home.models import (
   FAQ
)
from authority.forms import FAQForm

# <<----------------- List, Add, Update, Delete FAQ ---------------->>

# List FAQ
class FAQListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = FAQ
    template_name = 'faq/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'FAQ List'
        return context


# Update FAQ
class UpdateFAQView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = FAQ
    fields = ['question', 'answer']
    template_name = 'faq/add_update_faq.html'
    success_url = reverse_lazy('authority:faq_list')
    success_message = "FAQ Updated Successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update FAQ"
        context["updated"] = True
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


# Add FAQ
class AddFAQView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = FAQ
    fields = ['question', 'answer']
    template_name = 'faq/add_update_faq.html'
    success_url = reverse_lazy('authority:faq_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add FAQ"
        return context

    def form_valid(self, form):
        messages.success(self.request, "FAQ Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


# Delete FAQ
class FAQDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        faq = get_object_or_404(FAQ, pk=pk)
        faq.delete()
        messages.success(request, "FAQ deleted successfully.")
        return redirect('authority:faq_list')
