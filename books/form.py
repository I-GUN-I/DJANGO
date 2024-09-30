from django import forms
from .models import Category, Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'categories', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the author name'}),
            'description': forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': 'Enter the description of the book'}),
            'categories': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={'class': 'form-select'})
        }

