from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from books.models import Book
from django.contrib.auth.models import User
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@api_view(['POST'])
def checkout_book(request):
    """
    Request data: {"user_id": 1, "book_id": 2}
    """
    user_id = request.data.get('user_id')
    book_id = request.data.get('book_id')

    try:
        user = User.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
    except (User.DoesNotExist, Book.DoesNotExist):
        return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

    if book.copies_available < 1:
        return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already has this book
    if Transaction.objects.filter(user=user, book=book, is_returned=False).exists():
        return Response({"error": "User already checked out this book"}, status=status.HTTP_400_BAD_REQUEST)

    # Create transaction
    Transaction.objects.create(user=user, book=book)
    book.copies_available -= 1
    book.save()

    return Response({"message": f"{book.title} checked out by {user.username}"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def return_book(request):
    """
    Request data: {"user_id": 1, "book_id": 2}
    """
    user_id = request.data.get('user_id')
    book_id = request.data.get('book_id')

    try:
        transaction = Transaction.objects.get(user_id=user_id, book_id=book_id, is_returned=False)
    except Transaction.DoesNotExist:
        return Response({"error": "No active transaction found for this user and book"}, status=status.HTTP_404_NOT_FOUND)

    transaction.is_returned = True
    transaction.return_date = timezone.now()
    transaction.save()

    # Increment book copies
    book = transaction.book
    book.copies_available += 1
    book.save()

    return Response({"message": f"{book.title} returned by {transaction.user.username}"}, status=status.HTTP_200_OK)