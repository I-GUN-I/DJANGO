from rest_framework import serializers
from books.serializers import BookSerializer
from authen.serializers import UserSerializer
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = Loan
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date', 'is_returned', 'is_overdue']

class LoanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'user', 'borrow_date', 'return_date']
    
    def clean(self):
        cleaned_data = super().clean()
        date_return = cleaned_data['return_date']
        book = cleaned_data['book']
        date_now = timezone.now().date()
        max_date = date_now + timedelta(days=24)
        
        if date_return < date_now:
            raise ValidationError("Your return date is in the past.")

        if date_return > max_date:
            raise ValidationError("You can't borrow a book for more than 24 days.")
        
        if book.status == 'Unavailable':
            raise ValidationError("This book is currently unavailable.")

        return cleaned_data

class LoanReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'book', 'user', 'return_date', 'is_returned']