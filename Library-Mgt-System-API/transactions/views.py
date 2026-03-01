from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from users.models import CustomUser
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


class UserTransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Transaction.objects.filter(
            user_id=user_id
        ).order_by('-checkout_date')


class CheckoutBookView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, book_id, user_id):

        try:
            user = CustomUser.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            if Transaction.objects.filter(
                user=user,
                book=book,
                is_returned=False
            ).exists():
                return Response(
                    {"error": "User already has this book"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            

            if book.copies_available < 1:
                return Response(
                    {"error": "No copies available"},
                    status=status.HTTP_400_BAD_REQUEST
                )


            transaction = Transaction.objects.create(
                user=user,
                book=book,
                due_date=timezone.now() + timedelta(days=7)
            )

            book.copies_available -= 1
            book.save()

            return Response(
                {
                    "message": "Book checked out",
                    "transaction_id": transaction.id
                },
                status=status.HTTP_201_CREATED
            )

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)


class ReturnBookView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, transaction_id):

        try:
            transaction = Transaction.objects.get(id=transaction_id)

            if transaction.is_returned:
                return Response(
                    {"error": "Book already returned"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            transaction.return_date = timezone.now()
            transaction.is_returned = True
            transaction.save()

            book = transaction.book
            book.copies_available += 1
            book.save()

            return Response(
                {"message": "Book returned successfully"},
                status=status.HTTP_200_OK
            )

        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)