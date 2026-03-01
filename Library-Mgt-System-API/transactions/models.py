from django.db import models
from django.utils import timezone

from books.models import Book
from users.models import CustomUser


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Auto-calculate penalty if returned late
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            self.penalty = days_late * 1.00  # $1 per day

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"