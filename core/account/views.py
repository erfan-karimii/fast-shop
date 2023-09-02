from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages

from .forms import RegisterForm , LoginForm
from .models import User
# Create your views here.

def login_view(request):
    context = {

    }
    return render(request,'login.html',context)


def check_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('account:welcome')
            else:
                messages.error(request,'.کاربری با مشخصات وارده پیدا نشد')
                return redirect('account:login')

        else:
            messages.error(request,form.errors)
            return redirect('account:login')


def welcome_page_view(request):
    print(request.user)
    context = {

    }
    return render(request,'welcome.html',context)

def logout_view(request):
    logout(request)
    return redirect('home:home')

def register_view(request):
    context = {

    }
    return render(request,'register.html',context)

def check_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(email=email,password=password)
            login(request, user)
            return redirect('account:welcome')
        else:
            print(form.errors)
            messages.error(request,form.errors)
            return redirect('account:register')