from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password must be at least five characters long.'})
    )
    password_2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter the same password as above.'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        help_texts = {
            'username': ''
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username must be unique.'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name.'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name.'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        pwd_1 = cleaned_data['password_1']
        pwd_2 = cleaned_data['password_2']

        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")

        if pwd_1 != pwd_2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

class ProfileForm(forms.ModelForm):
    new_pwd = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password must be at least five characters long.'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': ''
        }

    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data['username']
        if self.instance.username != user_name:
            if User.objects.filter(username=user_name).exists():
                raise ValidationError("This username is already taken.")

        return cleaned_data
