from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import SignUpForm, ProfileForm
from rest_framework.authentication import TokenAuthentication

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('book-list') 
        return render(request, 'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('book-list')

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pwd = form.cleaned_data['password_1']

            user.set_password(pwd)
            user.save()

            group = Group.objects.get(name='User')
            user.groups.add(group)

            login(request, user)
            return redirect('book-list')

        return render(request, 'signup.html', {'form': form})

class ProfileView(LoginRequiredMixin, View):
    login_url = "/auth/"
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            pwd = form.cleaned_data['new_pwd']
            if pwd:
                request.user.set_password(pwd)
                request.user.save()
            
            form.save()
            return redirect('book-list')
        return render(request, 'profile.html', {'form': form})

class MyTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"
