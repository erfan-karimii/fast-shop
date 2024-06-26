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

    specification_dict = product.specification
 
    product.string1 = dict(list(specification_dict.items())[len(specification_dict)//2:]) 
    product.string2 = dict(list(specification_dict.items())[:len(specification_dict)//2])
         
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
        profile = Profile.objects.filter(user=request.user.id).first()
        print(request.POST)
    
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = profile
            comment.save()
            messages.success(request,"کامنت شما با موفقیت ثبت شد و پس از تایید مدریت نمایش داده خواهد شد.")
        else:
            messages.error(request,form.errors)
            
        return redirect(reverse("product:detail-view",args=[product_id]))


def list_view(request):
    categories = Category.objects.all()[:6]
    brands = Brand.objects.all()
    profile = Profile.objects.filter(user=request.user.id).first()
    wishlist = WishList.objects.filter(profile=profile).first()
    products = Product.objects.filter(is_show=True).order_by('-created_date')

    context = {
        'products' : products,
        'categories' : categories,
        'brands' : brands,
        'wishlist' : wishlist,
    }
    return render(request,'list-view.html',context)


def search_view(request):
    selected_colors = request.GET.getlist('colors','')
    selected_brands = request.GET.getlist('brands','')
    selected_order_by = request.GET.get('order_by','-created_date')
    selected_properties = '' #IMPORTANT (need implement as fast as possible)
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',1000000000)
    cat_id = request.GET.get('cat_id',1)
    category = Category.objects.get(id=cat_id)

    products = Product.objects.filter(is_show=True,price__gte=float(min_price),price__lte=float(max_price),
                                      category=category).order_by(selected_order_by)
    brands = category.brand.all()
    products = products.filter()

    if selected_brands:
        products = products.filter(brand__name__in=selected_brands)
    if selected_colors:
        products = products.filter(color__in=selected_colors)
    
    profile = Profile.objects.filter(user=request.user.id).first()
    wishlist = WishList.objects.filter(profile=profile).first()

    context = {
        'products' : products,
        'category' : category,
        'cat_id' : cat_id,
        'brands' : brands,
        'selected_colors' : selected_colors,
        'selected_brands' : selected_brands,
        'min_price' : min_price,
        'max_price' : max_price,
        'selected_order_by' : selected_order_by,
        'wishlist' : wishlist,
    }
    return render(request,'category-list-view.html',context)


def category_list_view(request,cat_id):
    category = Category.objects.get(id=cat_id)
    brands = category.brand.all()
    selected_order_by = request.GET.get('order_by','-created_date')
    products = Product.objects.filter(is_show=True,category=category).order_by(selected_order_by)
    profile = Profile.objects.filter(user=request.user.id).first()
    wishlist = WishList.objects.filter(profile=profile).first()
    
    context = {
        'category' : category, 
        'cat_id' : cat_id,
        'brands' : brands, 
        'products' : products,
        'selected_order_by' : selected_order_by, 
        'wishlist' : wishlist, 
    }

    return render(request,'category-list-view.html',context)


@login_required
def wishlist_view(request):
    profile = Profile.objects.filter(user=request.user.id).first()
    wishlist = WishList.objects.get(profile=profile)
    context = {
        'wishlist' : wishlist,

    }
    return render(request,'profile/profile-favorites.html',context)

@login_required
def remove_from_wishlist_view(request,id):
    product = Product.objects.get(id=id)
    profile = Profile.objects.filter(user=request.user.id).first()
    
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
    profile = Profile.objects.filter(user=request.user.id).first()
    
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

    