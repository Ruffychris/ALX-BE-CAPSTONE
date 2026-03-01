from django.core.mail import send_mail
from django.utils import timezone
from .models import Transaction

def notify_overdue_users():
    overdue = Transaction.objects.filter(is_returned=False, due_date__lt=timezone.now())
    for t in overdue:
        send_mail(
            'Overdue Book Notice',
            f'Hello {t.user.username}, the book "{t.book.title}" is overdue. Please return it to avoid penalties.',
            'library@example.com',
            [t.user.email],
        )