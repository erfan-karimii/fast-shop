from django.shortcuts import render

# Create your views here.

def detail_view(request,id):
    context = {

    }
    return render(request,'single-product.html',context)