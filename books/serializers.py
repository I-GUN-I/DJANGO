from rest_framework import serializers
from .models import Book
from category.serializers import CategorySerializer

class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'categories', 'status']

class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'categories']
    
    def validate(self, data):
        book_title = data['title']
        if self.instance.title != book_title:
            if Book.objects.filter(title=book_title).exists():
                raise serializers.ValidationError("This book already exists.")
        return data