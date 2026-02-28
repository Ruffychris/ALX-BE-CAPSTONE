from django.contrib import admin
from .models import Book, Member, Borrow, Return


admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Borrow)
admin.site.register(Return)