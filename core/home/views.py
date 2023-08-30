from django.shortcuts import render
from .models import TemplateSettings , NavBar , Footer
# Create your views here.

def home_view(request):
    context = {

    }
    return render(request,'index.html',context)

def header_view(request):
    context = {
        'template_setting' : TemplateSettings.objects.last(),
        'navbars' : NavBar.objects.all(),
    }
    return render(request,'header.html',context)

def footer_view(request):
    context = {
        'template_setting' : TemplateSettings.objects.last(),
        "footers" : Footer.objects.all(),
    }
    return render(request,'footer.html',context)