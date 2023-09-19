from django.shortcuts import render , get_object_or_404 , redirect 
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product , Category , WishList
from .forms import CommentForm
from home.models import TemplateSettings , Brand
from account.models import Profile 
# Create your views here.

def detail_view(request,id):
    product = get_object_or_404(Product,id=id)
    
    lines = product.specification = product.specification.strip().split('\n')
    half = len(lines) // 2

    product.string1 = lines[:half]
    product.string2 = lines[half:]
    form = CommentForm()
    context = {
        'product':product,
        'template_setting' : TemplateSettings.objects.last(),
        'form' : form,
    }
    return render(request,'single-product.html',context)

@login_required
def validate_comment_view(request):
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


def list_view(request,cat_id=None):
    categories = Category.objects.all()[:6]
    brands = Brand.objects.all()
    profile = Profile.objects.get(user=request.user)
    wishlist = WishList.objects.get(profile=profile)
    
    selected_colors = request.GET.getlist('colors','')
    selected_brands = request.GET.getlist('brands','')
    order_by = request.GET.get('order_by','-created_date')
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',1000000000)

    products = Product.objects.filter(is_show=True,price__gte=float(min_price),price__lte=float(max_price))
    category = None
    if cat_id:
        category = Category.objects.get(id=cat_id)
        brands = category.brand.all()
        products = products.filter(category=category)

    if selected_brands:
        products = products.filter(brand__name__in=selected_brands)
    if selected_colors:
        products = products.filter(color__in=selected_colors)
    if order_by:
        products = products.order_by(order_by)

    context = {
        'products' : products,
        'categories' : categories,
        'brands' : brands,
        'selected_colors' : selected_colors,
        'selected_brands' : selected_brands,
        'min_price' : min_price,
        'max_price' : max_price,
        'category' : category,
        'order_by' : order_by,
        'wishlist' : wishlist,
    }
    return render(request,'list-view.html',context)

@login_required
def wishlist_view(request):
    profile = Profile.objects.get(user=request.user)
    wishlist = WishList.objects.get(profile=profile)
    context = {
        'wishlist' : wishlist,

    }
    return render(request,'profile/profile-favorites.html',context)

@login_required
def remove_from_wishlist_view(request,id):
    product = Product.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    
    wishlist = WishList.objects.get(profile=profile)
    if product in wishlist.product.all():
        wishlist.product.remove(product)
        messages.success(request,"محصول از لیست علاقه مندی شما حذف شد.")
        return redirect('product:wishlist')  


def add_to_wishlist_ajax(request):
    if request.user.is_anonymous :
        message = 'لطفا برای افزودن محصول به لیست علاقه مندی های خود , وارد حساب کاربری خود شوید.'
        icon = 'error'
        return JsonResponse({'message':message,'icon':icon})
    
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    profile = Profile.objects.get(user=request.user)
    
    wishlist , created = WishList.objects.get_or_create(profile=profile)
    if product in wishlist.product.all():
        wishlist.product.remove(product)
        message = "محصول از لیست علاقه مندی شما حذف شد."
        icon = 'info'
        css_class = 'search_icon_like_2'
    else:
        wishlist.product.add(product)
        message = "محصول به لیست علاقه مندی شما اضافه شد."
        icon = 'success'
        css_class = 'search_icon_like'
    wishlist.save()
    return JsonResponse({'message':message,'icon':icon,'id':product.id,'css_class':css_class})

    