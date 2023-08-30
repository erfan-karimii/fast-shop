from django.shortcuts import render , get_object_or_404
from django.urls import reverse
from .models import Product
from .forms import CommentForm
from home.models import TemplateSettings
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
        form = CommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print('pass')
        else:
            print(form.errors)
            
        return reverse("product:detail-view",args=[42])