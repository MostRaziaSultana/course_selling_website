from django.contrib import admin
from.models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_verified')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('is_verified',)
