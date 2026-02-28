from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDestroyView
from .views import checkout_book, return_book

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
    path('transactions/checkout/', checkout_book, name='checkout-book'),
    path('transactions/return/', return_book, name='return-book'),
]