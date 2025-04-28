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
from Course.models import (
   CourseCategory,Course,CoursePurchase
)
from authority.forms import CourseForm,CourseCategoryForm,CoursePurchaseForm

# <<----------------- List, Add, Update, Delete Course Category ---------------->>

class CourseCategoryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = CourseCategory
    template_name = 'courses/course_category_list.html'
    context_object_name = 'course_categories'
    paginate_by = 10

    def get_queryset(self):
        return CourseCategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Categories'
        return context


# Update CourseCategory
class UpdateCourseCategoryView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = CourseCategory
    fields = ['name']
    template_name = 'courses/add_update_course_category.html'
    success_url = reverse_lazy('authority:course_category_list')
    success_message = "Course Category Updated Successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Course Category"
        context["updated"] = True
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


# Add CourseCategory
class AddCourseCategoryView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = CourseCategory
    fields = ['name']
    template_name = 'courses/add_update_course_category.html'
    success_url = reverse_lazy('authority:course_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Course Category"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Course Category Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


# Delete CourseCategory
class CourseCategoryDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        category = get_object_or_404(CourseCategory, pk=pk)
        category.delete()
        messages.success(request, "Course Category deleted successfully.")
        return redirect('authority:course_category_list')


# <<----------------- List, Add, Update, Delete Course  ---------------->>


class CourseListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        return Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Courses'
        return context


class UpdateCourseView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'category', 'image', 'price']
    template_name = 'courses/add_update_course.html'
    success_url = reverse_lazy('authority:course_list')
    success_message = "Course Updated Successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Course"
        context["updated"] = True
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AddCourseView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description', 'category', 'image', 'price']
    template_name = 'courses/add_update_course.html'
    success_url = reverse_lazy('authority:course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Course"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Course Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class CourseDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('authority:course_list')


# <<----------------- List, Update, Delete Course Purchase ---------------->>


# List View
class CoursePurchaseListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = CoursePurchase
    template_name = 'courses/course_purchase_list.html'
    context_object_name = 'purchases'
    paginate_by = 10

    def get_queryset(self):
        return CoursePurchase.objects.select_related('user', 'course').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Purchases'
        return context

# Update View
class UpdateCoursePurchaseView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = CoursePurchase
    form_class = CoursePurchaseForm
    template_name = 'courses/update_course_purchase.html'
    success_url = reverse_lazy('authority:course_purchase_list')
    success_message = "Purchase updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Purchase"
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)

# Delete View
class CoursePurchaseDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        purchase = get_object_or_404(CoursePurchase, pk=pk)
        purchase.delete()
        messages.success(request, "Purchase deleted successfully.")
        return redirect('authority:course_purchase_list')