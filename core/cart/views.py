from django.shortcuts import render , redirect
import json
import ast

from .forms import NewOrderForm
from product.models import Product
# Create your views here.


def cart_view(request):
    orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))
    products = Product.objects.filter(id__in=orderdetail.keys())
    counts = list(orderdetail.values())
    for index,product in enumerate(products) :
        product.customer_count = counts[index]

    context = {
        'products' : products,
    }
    return render(request,'cart.html',context)

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