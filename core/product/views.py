from django.shortcuts import render , get_object_or_404 , redirect 
from django.urls import reverse
from .models import Product
from .forms import CommentForm
from home.models import TemplateSettings
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