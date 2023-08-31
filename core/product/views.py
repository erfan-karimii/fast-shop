from django.shortcuts import render , get_object_or_404 , redirect 
from django.urls import reverse
from .models import Product , Category
from .forms import CommentForm , ProductFilterForm
from home.models import TemplateSettings , Brand
from account.models import Profile 
# Create your views here.

def detail_view(request,id):
    product = get_object_or_404(Product,id=id)
    
    lines = product.specification = product.specification.strip().split('\n')
    half = len(lines) // 2

    product.string1 = lines[:half]
    product.string2 = lines[half:]

    context = {
        'product':product,
        'template_setting' : TemplateSettings.objects.last(),
    }
    return render(request,'single-product.html',context)

def validate_comment(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product,id=product_id)
        profile = Profile.objects.get(user=request.user)
    
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = profile
            comment.save()
        else:
            print(form.errors)
            
        return redirect(reverse("product:detail-view",args=[product_id]))

def list_view(request):
    products = Product.objects.filter(is_show=True)
    categories = Category.objects.all()[:6]
    brands = Brand.objects.all()
    if len(request.GET):
        colors = request.GET.getlist('colors','')
        brands_id = request.GET.getlist('brands','')
        # if brands_id:
        #     products = products.filter(brand__id__in=brands_id)
        if colors:
            # colors_text = ' '.join(colors)
            # print(colors_text)
            products = products.filter(specification__in=colors)
        
        # print('yes' if 'سفید' in Product.objects.get(id=2).specification else 'no')


        # form = ProductFilterForm(request.GET)
        # if form.is_valid():
            # colors = form.clean_brands()
            # brands_id= form.cleaned_data('brands')
            # products.filter(specification__in = colors ,brand__id__in=brands_id)
        #     print(products)
        # else:
        #     print(form.errors)
            


    context = {
        'products' : products,
        'categories' : categories,
        'brands' : brands,

    }
    return render(request,'list-view.html',context)