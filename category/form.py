from django import forms
from .models import Category
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter category description'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cat_name = cleaned_data['name']

        if self.instance.name != cat_name:
            if Category.objects.filter(name=cat_name).exists():
                raise ValidationError("This Category already exists.")

        return cleaned_data
