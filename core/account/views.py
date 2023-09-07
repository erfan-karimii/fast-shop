from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


from .forms import RegisterForm , LoginForm , ProfileEditForm , ResetPassword
from .models import User,Profile , ProfileMessage
from cart.models import Order
# Create your views here.

def login_view(request):
    next_url = request.GET.get('next',None)
    context = {
        'next_url' : next_url
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
                return redirect(request.POST.get('next-url') or 'account:welcome')
            else:
                messages.error(request,'.کاربری با مشخصات وارده پیدا نشد')
                return redirect('account:login')

        else:
            messages.error(request,form.errors)
            return redirect('account:login')


def welcome_page_view(request):
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
    delivered_orders_count = Order.objects.filter(profile=profile,order_status='delivered').count()
    cancelled_orders_count = Order.objects.filter(profile=profile,order_status='cancelled').count()
    current_orders_count = Order.objects.filter(Q(profile=profile) & (Q(order_status='in_proccesing')|Q(order_status='sended'))).count()

    context = {
        "cancelled_orders_count":cancelled_orders_count,
        "delivered_orders_count":delivered_orders_count,
        "current_orders_count":current_orders_count,
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
        profile = Profile.objects.get(user=request.user)
        form = ProfileEditForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'پروفایل شما با موفقیت ویرایش شد.')
        else:
            messages.error(request,form.errors)
        
        return redirect("account:profile")


@login_required
def current_order_view(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(Q(profile=profile) & (Q(order_status='in_proccesing')|Q(order_status='sended')))
    context = {
        'orders' : orders , 
    }
    return render(request,'profile/order-current.html',context)


@login_required
def cancelled_order_view(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(profile=profile,order_status='cancelled')
    context = {
        'orders' : orders , 
    }
    return render(request,'profile/order-cancelled.html',context)


@login_required
def delivered_order_view(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(profile=profile,order_status='delivered')
    context = {
        'orders' : orders , 
    }

    return render(request,'profile/order-delivered.html',context)



@login_required
def message_page_view(request):
    profile = Profile.objects.get(user=request.user)
    profile_messages = ProfileMessage.objects.filter(profile=profile).order_by('-created_date') 
    context = {
        'profile_messages' : profile_messages
    }
    return render(request,'profile/order-message.html',context)


@login_required
def product_received_view(request):
    order_id = request.GET.get('order_id',None)
    user_profile = Profile.objects.get(user=request.user)
    order = Order.objects.get(id=order_id)

    if order_id and order.profile == user_profile:
        order.order_status = 'delivered'
        order.save()
    
    message = f'سفارش شما با کد {order.shopping_id} تحویل داده شد .تجربه خریدت برامون مهمه.'
    ProfileMessage.objects.create(profile = user_profile,message = message)
    messages.success(request,message)
    return redirect('account:profile')
 

@login_required
def cancel_order_view(request):
    order_id = request.GET.get('order_id',None)
    user_profile = Profile.objects.get(user=request.user)
    order = Order.objects.get(id=order_id)

    if order_id and order.profile == user_profile:
        order.order_status = 'cancelled'
        order.save()
    
    message = f'سفارش شما با کد {order.shopping_id}لغو شد .هزینه سفارش شما طی 72 ساعت کاری آینده به حساب شما واریز خواهد شد..'
    ProfileMessage.objects.create(profile = user_profile,message = message)
    messages.error(request,message)
    return redirect('account:profile')

