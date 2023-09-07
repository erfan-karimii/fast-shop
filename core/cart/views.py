from django.shortcuts import render , redirect
from django.http import Http404 
from django.contrib import messages

import ast

from .forms import NewOrderForm
from product.models import Product
# Create your views here.

def check_cookies(cookie):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
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

def add_to_cart_view(request):
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

def change_orderitem_count_view(request):
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


def remove_from_cart_view(request):
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