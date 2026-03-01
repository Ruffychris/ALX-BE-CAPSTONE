from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    published_date = models.DateField(null=True, blank=True)
    copies_available = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <- use this
        on_delete=models.CASCADE
    )
    membership_date = models.DateField()


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member} - {self.book}"


class Return(models.Model):
    borrow = models.OneToOneField(Borrow, on_delete=models.CASCADE)
    return_date = models.DateField(auto_now_add=True)
    fine_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"Return - {self.borrow}"