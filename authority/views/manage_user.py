from django.urls import reverse_lazy
from django.shortcuts import redirect,reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout
from django.views.generic import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import AuthenticationForm
# class-based view classes
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.edit import FormView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

#Import Filter Classes
from authority.filters import UserListFilter


# Models Accounts
from django.contrib.auth.models import User

#Import From
from authority.forms import UserInfoForm,AddAdminUserForm,UpdateAdminUserForm,ResetPasswordForm


class UserListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    queryset = User.objects.filter(is_active=True)
    filterset_class = UserListFilter
    template_name = 'user/user_list.html'
    paginate_by = 6

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=self.queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User List"
        context["users"] =  self.filterset_class(self.request.GET, queryset=self.queryset)
        return context



class CustomLoginView(FormView):
    template_name = 'user/custom_login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('authority:authority_admin')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        username = form.data.get('username')
        password = form.data.get('password')
        remember_me = form.data.get('remember_me')

        if form.is_valid():
            user = authenticate(self.request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(self.request, user)

                if remember_me:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(18000)

                next_url = request.GET.get('next', self.success_url)

                if url_has_allowed_host_and_scheme(next_url, allowed_hosts=self.request.get_host()):
                    return redirect(next_url)
                else:
                    messages.error(self.request, 'Invalid redirect URL.')
                    return redirect(self.success_url)
            else:
                messages.error(self.request, 'Invalid username, password, or insufficient permissions.')
                return redirect(request.path)
        else:
            messages.error(self.request, 'Invalid username or password.')
            return redirect(request.path)


class CustomLogoutView(View):
    success_url = reverse_lazy('authority:login')
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect(self.success_url)



class AddAdminUserView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = User
    form_class = AddAdminUserForm
    template_name = 'user/add_admin.html'
    success_url = reverse_lazy('authority:user_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Admin user added successfully!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                if 'Password must contain at least 8 characters.' in error:
                    messages.error(self.request, 'The password must be at least 8 characters long.')
                elif 'Password cannot be entirely numeric.' in error:
                    messages.error(self.request, 'The password cannot be entirely numeric.')
                elif 'Password is too common.' in error:
                    messages.error(self.request, 'The password is too common.')
                elif 'Password cannot be too similar to the username.' in error:
                    messages.error(self.request, 'The password cannot be too similar to the username.')

        return self.render_to_response(self.get_context_data(form=form))

class UpdateAdminUserView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateAdminUserForm
    template_name = 'user/update_admin.html'
    success_url = reverse_lazy('authority:profile_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Admin user updated successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating the admin user.')
        return self.render_to_response(self.get_context_data(form=form))

class ProfileListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    queryset = User.objects.filter(is_active=True)
    filterset_class = UserListFilter
    template_name = 'user/profile_list.html'
    paginate_by = 6

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=self.queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User List"
        context["users"] =  self.filterset_class(self.request.GET, queryset=self.queryset)
        return context


class DeleteUserView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = User
    template_name = 'authority/confirm_delete.html'
    context_object_name = 'user'

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # Prevent deletion of own account
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect('authority:user_list')

        if user.is_superuser and not request.user == user:
            if request.user.is_superuser:
                user.delete()
                messages.success(request, "Superuser deleted successfully.")
                return redirect('authority:user_list')
            else:
                messages.error(request, "You cannot delete a superuser unless you're also a superuser.")
                return redirect('authority:user_list')

        # If it's not a superuser, proceed with deletion
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('authority:user_list')

class PasswordResetView(LoginRequiredMixin, AdminPassesTestMixin, FormView):
    template_name = 'user/reset_password.html'
    form_class = ResetPasswordForm

    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        self.user = get_object_or_404(User, id=user_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user == self.user:
            return reverse('authority:login')
        else:
            return reverse('authority:update_admin', kwargs={'pk': self.user.id})

    def form_valid(self, form):
        new_password = form.cleaned_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        messages.get_messages(self.request).used = True

        if self.request.user == self.user:
            messages.success(self.request, 'Your password has been updated. Please log in again.')
            return redirect(self.get_success_url())

        update_session_auth_hash(self.request, self.user)
        messages.success(self.request, f"Password for {self.user.username} updated successfully!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.get_messages(self.request).used = True
        for field, errors in form.errors.items():
            for error in errors:
                if 'Password must contain at least 8 characters.' in error:
                    messages.error(self.request, 'The password must be at least 8 characters long.')
                elif 'Password cannot be entirely numeric.' in error:
                    messages.error(self.request, 'The password cannot be entirely numeric.')
                elif 'Password is too common.' in error:
                    messages.error(self.request, 'The password is too common.')
                elif 'Password cannot be too similar to the username.' in error:
                    messages.error(self.request, 'The password cannot be too similar to the username.')
                elif 'Passwords do not match.' in error:
                    messages.error(self.request, 'The passwords do not match.')

        return redirect('authority:reset_password', user_id=self.user.id)