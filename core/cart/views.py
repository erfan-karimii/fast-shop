from django.shortcuts import render , redirect
from django.http import Http404 ,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import ast

from .forms import NewOrderForm , CheckOrderFields
from .models import Order , OrderItem
from product.models import Product
from account.models import Profile , ProfileMessage
# Create your views here.


def check_cookies(cookies):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if isinstance(cookies,str):
                kwargs.update({cookies:cookies in request.COOKIES,})
            else:
                for cookie in cookies:
                    kwargs.update({cookie:cookie in request.COOKIES,})
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@check_cookies('orderdetail')
def cart_view(request,**kwargs):
    if kwargs.get('orderdetail') and request.COOKIES.get('orderdetail') != '{}' :
        orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))
        products = Product.objects.filter(id__in=orderdetail.keys())
        total_price = 0

        for product in products :
            product.customer_count = orderdetail[product.id]
            total_price += product.calculate_price(product.customer_count)
    
        context = {
            'products' : products,
            'total_price' : total_price,
        }
        return render(request,'cart.html',context)
    
    else:
        return render(request,'cart-empty.html')


@check_cookies('orderdetail')
def add_to_cart_view(request,**kwargs):
    if kwargs.get('orderdetail'):
        form = NewOrderForm(request.GET or None)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']    
            
            orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))

            if product_id in orderdetail:
                orderdetail[product_id] += 1
            else:
                orderdetail[product_id] = 1

            response = redirect('/cart/')
            response.set_cookie('orderdetail',orderdetail,172800)
            return response 
        else:
            print(form.errors)
            return redirect('/')
    else:
        return redirect('/')


@check_cookies('orderdetail')
def change_orderitem_count_view(request,**kwargs):
    if kwargs.get('orderdetail'):
        product_id = int(request.GET.get("product_id"))
        count = int(request.GET.get('count'))
        orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))

        if product_id in orderdetail:
            orderdetail[product_id] = count
        else:
            raise Http404()
        
        messages.success(request,'تعداد محصول با موفقیت تغییر پیدا کرد.')
        response = redirect('/cart/')
        response.set_cookie('orderdetail',orderdetail,172800)
        return response 
    else:
        return redirect('/')


@check_cookies('orderdetail')
def remove_from_cart_view(request,**kwargs):
    if kwargs.get('orderdetail'):
        product_id = int(request.GET.get("product_id"))
        orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))

        if product_id in orderdetail:
            del orderdetail[product_id]
        else:
            raise Http404()


        messages.success(request,'محصول با موفقیت حذف شد.')
        response = redirect('/cart/')
        response.set_cookie('orderdetail',orderdetail,172800)
        return response 
    else:
        return redirect('/')

@login_required    
@check_cookies('orderdetail')
def confirm_order_view(request,**kwargs):
    if kwargs.get('orderdetail') and request.COOKIES.get('orderdetail') != '{}':
        orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))
        products = Product.objects.filter(id__in=orderdetail.keys())
        total_price = 0

        for product in products :
            product.customer_count = orderdetail[product.id]
            total_price += product.calculate_price(product.customer_count)

        context = {
            'products' : products,
            'total_price' : total_price,
        }
    else:
        return redirect('/')
    return render(request,'confirm-order.html',context)

@login_required    
def user_recipient_ajax(request):
    profile = Profile.objects.get(user= request.user)
    first_name = profile.first_name
    last_name = profile.last_name
    phone_number = profile.phone_number
    zip_code = profile.zip_code
    national_code = profile.national_code
    address = profile.address
    properties = {'first_name' : first_name,'last_name' : last_name,'phone_number' : phone_number,'zip_code' : zip_code,'national_code' : national_code,'address' : address}
    return JsonResponse(properties)


@login_required    
def check_confirm_order_view(request):
    if request.method == 'POST':
        form = CheckOrderFields(request.POST)
        if form.is_valid():
            mydict = {k: str(v).encode("utf-8") for k,v in form.cleaned_data.items()}
            response = redirect('cart:shopping_payment')
            response.set_cookie('order',mydict,172800)
            return response
        else:
            print(form.errors)
            return redirect('cart:confirm_order')
    else:
        return redirect('/')


@login_required    
@check_cookies(['order','orderdetail'])
def shopping_payment_view(request,**kwargs):
    if kwargs.get('order') and kwargs.get('orderdetail') and request.COOKIES.get('orderdetail') != '{}' :
        orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))
        products = Product.objects.filter(id__in=orderdetail.keys())
        total_price = 0

        for product in products :
            product.customer_count = orderdetail[product.id]
            total_price += product.calculate_price(product.customer_count)
        
        context = {
            'total_price' : total_price
        }     
        return render(request,'shopping-payment.html',context)
    else:
        return redirect('/')


@login_required    
@check_cookies(['order','orderdetail'])
def successful_payment_view(request,**kwargs):
    if kwargs.get('order') and kwargs.get('orderdetail') and request.COOKIES.get('orderdetail') != '{}' :
        profile = Profile.objects.get(user=request.user)

        orderdetail_cookie = request.COOKIES.get('orderdetail')
        orderdetail = ast.literal_eval(orderdetail_cookie)
        products = Product.objects.filter(id__in=orderdetail.keys())

        total_price = 0
        for product in products :
            product.customer_count = orderdetail[product.id]
            product.count -= product.customer_count
            product.sales_number += product.customer_count
            total_price += product.calculate_price(product.customer_count)
            product.save()

        order_cookie = request.COOKIES.get('order')
        order = ast.literal_eval(order_cookie)
        order_right_value = {k: v.decode("utf-8") for k,v in order.items()}
        ## validate with form

        order = Order.objects.create(**order_right_value,profile=profile,paid_amount=total_price,
                                     order_status='in_proccesing',payment_date=timezone.now())
        order_items = [
            OrderItem(order=order,product=product,price=product.main_discount_call(),
                      quantity=product.customer_count)
            for product in products
        ]        
        OrderItem.objects.bulk_create(order_items)

        message = f' سفارش شما با کد {order.shopping_id} ثبت شده و در حال پردازش است.'
        ProfileMessage.objects.create(profile=profile,message=message)

        response = render(request,'successful-payment.html',{'order_id':order.shopping_id})
        response.delete_cookie('order')
        response.set_cookie('orderdetail',{},172800)
        return response
    else:
        return redirect('/')


def unsuccessful_payment_view(request):
    return render(request,'unsuccessful-payment.html')
