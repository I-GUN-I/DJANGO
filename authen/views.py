from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .form import SignUpForm
from django.db import IntegrityError


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('book-list') 

        return render(request,'login.html', {"form":form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                pwd = form.cleaned_data['password_1']
                user.set_password(pwd)
                user.save()

                group = Group.objects.get(name='Borrower')
                user.groups.add(group)

                login(request, user)
                return redirect('book-list') 
            except IntegrityError:
                messages.error(request, "Username already exists")

        return render(request, 'signup.html', {'form': form})