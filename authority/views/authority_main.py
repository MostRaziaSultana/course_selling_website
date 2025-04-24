from django.shortcuts import redirect
from datetime import timedelta
from datetime import date
from django.db.models import Sum
from django.urls import reverse_lazy


# class-based view classes
from django.views.generic import TemplateView
from django.views.generic import ListView

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from django.contrib.auth.models import User



# Create your views here.
class AdminView(LoginRequiredMixin,AdminPassesTestMixin,TemplateView):
    template_name = 'authority/admin.html'
    login_url = reverse_lazy('authority:login')
    success_url = reverse_lazy('authority:authority_admin'),


