from django.shortcuts import render , redirect
from .forms import LoginForm
# Create your views here.

def login_view(request):
    context = {

    }
    return render(request,'login.html',context)


def check_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors)

    return redirect('account:welcome')

def welcome_page_view(request):
    context = {

    }
    return render(request,'welcome.html',context)


