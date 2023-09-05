from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm , LoginForm , ProfileEditForm , ResetPassword
from .models import User,Profile
# Create your views here.

def login_view(request):
    context = {

    }
    return render(request,'account/login.html',context)


def check_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next') or 'account:welcome')
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
    return render(request,'account/welcome.html',context)

@login_required
def logout_view(request):
    logout(request)
    messages.error(request,'شما از حساب کاربری خود خارج شدید.')
    return redirect('home:home')


def register_view(request):
    context = {

    }
    return render(request,'account/register.html',context)


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


@login_required
def reset_password_view(request):
    return render(request,'account/reset-password.html')

@login_required
def check_reset_password_view(request):
    if request.method == 'POST':
        form = ResetPassword(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            last_password = form.cleaned_data['last_password']
            password = form.cleaned_data['password']
            user = authenticate(request, email=request.user.email, password=last_password)
            if user is not None:
                user.set_password(password)
                user.save()
                messages.success(request,'.پسورد شما با موفقیت تغییر پیدا کرد')
                return redirect('account:login')
            else:
                messages.error(request,'.کاربری با مشخصات وارده پیدا نشد')
                return redirect('account:reset_password')

        else:
            messages.error(request,form.errors)
            return redirect('account:reset_password')


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile' : profile,
    }
    return render(request,'profile/profile.html',context)

@login_required
def sidebar_view(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile' : profile,
    }
    return render(request,'profile/sidebar.html',context)

@login_required
def profile_edit_view(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile' : profile,
    }
    return render(request,'profile/edit-profile.html',context)

@login_required
def check_profile_edit_view(request):
    if request.method == 'POST':
        print(request.POST,request.FILES)
        profile = Profile.objects.get(user=request.user)
        form = ProfileEditForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'پروفایل شما با موفقیت ویرایش شد.')
        else:
            messages.error(request,form.errors)
        
        return redirect("account:profile")
        


