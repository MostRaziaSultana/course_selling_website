from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Home.models import Brand

from authority.forms import BrandForm

# <<----------------- List, Add, Update, Delete Brand ---------------->>
class BrandListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    queryset = Brand.objects.all()
    template_name = 'brand/brand_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Brand.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Brand List"
        return context


class UpdateBrandView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brand/add_update_brand.html'
    success_url = reverse_lazy('authority:brand_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Brand"
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Brand Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again!")
        return super().form_invalid(form)


class AddBrandView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brand/add_update_brand.html'
    success_url = reverse_lazy('authority:brand_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Brand"

        return context

    def form_valid(self, form):
        messages.success(self.request, "Brand Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again!")
        return super().form_invalid(form)


class BrandDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        brand.delete()
        messages.success(request, "Brand deleted successfully.")
        return redirect('authority:brand_list')
