import django_filters
from django import forms
from django.db.models import Q

from django.contrib.auth.models import User

class UserListFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_all_fields',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by email or first name'})
    )

    class Meta:
        model = User
        fields = ['search']

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(email__icontains=value) | Q(first_name__icontains=value)
        )
        

        

