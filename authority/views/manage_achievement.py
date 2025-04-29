from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from Home.models import Achievement
from authority.forms import AchievementForm


class AchievementListView(LoginRequiredMixin, ListView):
    model = Achievement
    template_name = 'achievement/achievement_list.html'
    context_object_name = 'achievements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Achievement List'
        return context


class AddAchievementView(LoginRequiredMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievement/add_update_achievement.html'
    success_url = reverse_lazy('authority:achievement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Achievement"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Achievement Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class UpdateAchievementView(LoginRequiredMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievement/add_update_achievement.html'
    success_url = reverse_lazy('authority:achievement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Achievement"
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Achievement Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again!")
        return super().form_invalid(form)


class AchievementDeleteView(LoginRequiredMixin, DeleteView):
    def post(self, request, pk):
        achievement = get_object_or_404(Achievement, pk=pk)
        achievement.delete()
        messages.success(request, "Achievement deleted successfully.")
        return redirect('authority:achievement_list')
