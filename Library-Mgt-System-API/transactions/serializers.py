from rest_framework import serializers
from .models import Transaction
from books.serializers import BookSerializer
from django.contrib.auth.models import User

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date', 'is_returned']