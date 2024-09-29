from django import forms
from .models import Category
from books.models import Book
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'})
    )