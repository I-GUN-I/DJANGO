from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        help_text="Password must be at least five characters long."
    )
    password_2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
        help_text="Enter the same password as above."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        help_texts = {
            'username': 'Must be unique.',
            'first_name': 'Enter your first name.',
            'last_name': 'Enter your last name.',
        }

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")

        pwd_1 = cleaned_data['password_1']
        pwd_2 = cleaned_data['password_2']
        if pwd_1 != pwd_2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
