from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'checkout_date', 'return_date', 'is_returned')
    list_filter = ('is_returned',)
    search_fields = ('user__username', 'book__title')