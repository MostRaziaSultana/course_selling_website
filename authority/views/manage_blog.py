from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Import Models
from Home.models import Blog,BlogCategory

from authority.forms import BlogForm,BlogCategoryForm

# <<----------------- List, Add, Update, Delete Blog ---------------->>


class BlogListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog List'
        return context


class UpdateBlogView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/add_update_blog.html'
    success_url = reverse_lazy('authority:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Blog"
        context["updated"] = True
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AddBlogView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/add_update_blog.html'
    success_url = reverse_lazy('authority:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Blog"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Blog Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class BlogDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('authority:blog_list')



# <<----------------- List, Add, Update, Delete Blog Category ---------------->>
class BlogCategoryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = BlogCategory
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        return BlogCategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog Categories'
        return context


class UpdateBlogCategoryView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'blog/add_update_category.html'
    success_url = reverse_lazy('authority:blog_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Blog Category"
        context["updated"] = True
        return context
    def form_valid(self, form):
        messages.success(self.request, "Blog Category Updated Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AddBlogCategoryView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'blog/add_update_category.html'
    success_url = reverse_lazy('authority:blog_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Blog Category"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Blog Category Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class BlogCategoryDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    def post(self, request, pk):
        category = get_object_or_404(BlogCategory, pk=pk)
        category.delete()
        messages.success(request, "Blog Category deleted successfully.")
        return redirect('authority:blog_category_list')

