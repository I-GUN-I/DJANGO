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
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Username must be unique.'}),
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

        if len(pwd_1) < 5:
            raise ValidationError("Your new Password must be at least five characters long.")

        if pwd_1 != pwd_2:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data


class ProfileForm(forms.ModelForm):
    current_pwd = forms.CharField(
        label="Your Password (Required for change)",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password.'})
    )
    new_pwd = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password must be at least five characters long.'}),
        required=False
    )
    new_pwd_2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter the same password as above.'}),
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
        name = cleaned_data['username']
        mail = cleaned_data['email']
        pwd = cleaned_data['current_pwd']
        pwd_1 = cleaned_data['new_pwd']
        pwd_2 = cleaned_data['new_pwd_2']

        if not self.instance.check_password(pwd):
            raise ValidationError("The current password is incorrect.")

        if self.instance.username != name:
            if User.objects.filter(username=name).exists():
                raise ValidationError("This username is already taken.")

        if self.instance.email != mail:
            if User.objects.filter(email=mail).exists():
                raise ValidationError("This email is already be use by another account.")

        if len(pwd_1) < 5:
            raise ValidationError("Your new Password must be at least five characters long.")

        if pwd_1 != pwd_2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

