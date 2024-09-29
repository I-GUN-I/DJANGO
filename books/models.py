from django.db import models
from category.models import Category

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=55, choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], default='Available')
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.title
