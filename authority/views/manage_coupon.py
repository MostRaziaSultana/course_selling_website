from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin
from django.db.models import Count
from django.core.paginator import Paginator

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

# class-based view classes
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Course.models import (
   Coupon
)


# Import Forms
from authority.forms import (
    CouponForm
)

class CouponListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = Coupon
    template_name = 'coupon/coupon_list.html'
    context_object_name = 'coupon_list'
    paginate_by = 6

    def get_queryset(self):
        return Coupon.objects.annotate(user_count=Count('used_by')).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Coupon List"
        return context


class AddCouponView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Coupon
    template_name = 'coupon/add_update_coupon.html'
    form_class = CouponForm
    success_url = reverse_lazy('authority:coupon_list')

    def form_valid(self, form):
        messages.success(self.request, "Coupon created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Coupon"
        return context
class CouponUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Coupon
    template_name = 'coupon/add_update_coupon.html'
    form_class = CouponForm
    success_url = reverse_lazy('authority:coupon_list')  # Update with the correct URL name

    def form_valid(self, form):
        messages.success(self.request, "Coupon updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Coupon"
        context["updated"] = True  # Ensure this is set to True for updates
        return context


class CouponDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        coupon.delete()
        messages.success(request, "Coupon deleted successfully.")
        return redirect('authority:coupon_list')