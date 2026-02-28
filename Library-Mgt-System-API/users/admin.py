from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_membership', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username',)