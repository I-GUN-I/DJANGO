from django import forms
from .models import Loan
from datetime import datetime, timedelta
from django.utils import timezone
from books.models import Book
from django.core.exceptions import ValidationError

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_return = cleaned_data['return_date']
        date_now = timezone.now().date()
        max_date = date_now + timedelta(days=24)
        
        if date_return < date_now:
            raise ValidationError("Your return date is in the past.")

        if date_return > max_date:
            raise ValidationError("You can't borrow a book for more than 24 days.")


        return cleaned_data