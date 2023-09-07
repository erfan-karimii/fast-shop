from django.shortcuts import render
from .models import TemplateSettings , NavBar , Footer
from product.models import Product
import ast

from cart.views import check_cookies
# Create your views here.

def home_view(request):
    context = {

    }
    return render(request,'index.html',context)

@check_cookies('orderdetail')
def header_view(request,**kwargs):
    if kwargs.get('orderdetail') and request.COOKIES.get('orderdetail') != '{}' :
        orderdetail = ast.literal_eval(request.COOKIES.get('orderdetail'))
        products = Product.objects.filter(id__in=orderdetail.keys())[:2]

        for product in products :
            product.customer_count = orderdetail[product.id]
    else:
        products = []
    

    context = {
        'template_setting' : TemplateSettings.objects.last(),
        'navbars' : NavBar.objects.all(),
        'products' : products,
    }
    return render(request,'header.html',context)

def footer_view(request):
    context = {
        'template_setting' : TemplateSettings.objects.last(),
        "footers" : Footer.objects.all(),
    }
    return render(request,'footer.html',context)