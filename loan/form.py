from django import forms
from .models import Loan
from books.models import Book

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
