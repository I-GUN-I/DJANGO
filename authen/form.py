from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password_1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        pwd_1 = cleaned_data.get('password_1')
        pwd_2 = cleaned_data.get('password_2')

        if pwd_1 and pwd_2 and pwd_1 != pwd_2:
            raise ValidationError("Passwords do not match")

        return cleaned_data
