from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField()
    is_returned = models.BooleanField(default=False)
