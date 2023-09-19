from django.shortcuts import render , redirect
from django.contrib import messages
import ast

from product.models import Product , Category
from .models import TemplateSettings , NavBar , Footer ,UnderSlider , Brand , ContactUsInfo , ContectUsKeeprt
from .forms import ContactUsKeeperForm

from cart.views import check_cookies
# Create your views here.

def home_view(request):
    under_sliders_1 = UnderSlider.objects.all()[:4]
    under_sliders_2 = UnderSlider.objects.all()[4:]
    carousel_products = Product.objects.all().order_by('-created_date')[:8]
    special_products = Product.objects.filter(is_special=True).order_by('-created_date')
    most_sell_products = Product.objects.all().order_by('-sales_number')[:8]
    categories_1 = Category.objects.all()[:6]
    categories_2 = Category.objects.all()[6:]
    brands = Brand.objects.all()
    context = {
        'template_setting' : TemplateSettings.objects.last(),
        'under_sliders_1' : under_sliders_1,
        'under_sliders_2' : under_sliders_2,
        'carousel_products' : carousel_products,
        'special_products' : special_products,
        'most_sell_products' : most_sell_products,
        'categories_1' : categories_1,
        'categories_2' : categories_2,
        'brands' : brands,
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

def about_us_view(request):
    return render(request,'about-us.html',{})

def contact_us_view(request):
    contact_us_info = ContactUsInfo.objects.last()
    form = ContactUsKeeperForm()
    context = {
        'contact_us_info' : contact_us_info,
        'form' : form,
    }
    return render(request,'contact-us.html',context)

def contact_us_keeper_view(request):
    if request.method == 'POST':
        form = ContactUsKeeperForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'پیام شما با موفقیت دریافت شد.')
        else:
            messages.error(request,form.errors)
    return redirect('home:contact_us')
    