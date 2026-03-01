from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
    UserTransactionHistoryView,
    CheckoutBookView,
    ReturnBookView,
)

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),

    path('history/<int:user_id>/', UserTransactionHistoryView.as_view(), name='user-history'),

    path('checkout/<int:book_id>/<int:user_id>/', CheckoutBookView.as_view(), name='checkout-book'),
    path('return/<int:transaction_id>/', ReturnBookView.as_view(), name='return-book'),
]