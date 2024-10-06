from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'categories']

class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'categories']
    
    def clean(self):
        cleaned_data = super().clean()
        book_title = cleaned_data['title']

        if self.instance.title != book_title:
            if Book.objects.filter(title=book_title).exists():
                raise ValidationError("This book already exists.")
        
        return cleaned_data