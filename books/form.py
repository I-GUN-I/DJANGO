from django import forms
from .models import Category, Book
from django.core.exceptions import ValidationError

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the author name'}),
            'description': forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': 'Enter the description of the book'}),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        book_title = cleaned_data['title']

        if self.instance.title != book_title:
            if Book.objects.filter(title=book_title).exists():
                raise ValidationError("This book already exists.")

        return cleaned_data
