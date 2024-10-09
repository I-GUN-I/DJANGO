from rest_framework import serializers
from books.serializers import BookSerializer
from authen.serializers import UserSerializer
from .models import Loan
from django.utils import timezone
from datetime import timedelta

class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = Loan
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date', 'is_returned', 'is_overdue']

class LoanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'return_date']
    
    def validate(self, data):
        date_return = data['return_date']
        book = data['book']
        date_now = timezone.now().date()
        max_date = date_now + timedelta(days=24)
        
        if date_return < date_now:
            raise serializers.ValidationError("Your return date is in the past.")

        if date_return > max_date:
            raise serializers.ValidationError("You can't borrow a book for more than 24 days.")

        if book.status == 'Unavailable':
            raise serializers.ValidationError("This book is currently unavailable.")

        return data

class LoanReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'book', 'return_date', 'is_returned']