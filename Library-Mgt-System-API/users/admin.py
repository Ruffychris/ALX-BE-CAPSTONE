from django.contrib import admin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_of_membership', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username',)