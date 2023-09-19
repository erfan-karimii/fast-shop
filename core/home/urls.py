from django.urls import path 
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.home_view,name='home'),
    path('header/',views.header_view,name='header'),
    path('footer/',views.footer_view,name='footer'),
    path('about_us/',views.about_us_view,name='about_us'),
    path('contact_us/',views.contact_us_view,name='contact_us'),
    path('contact_us_keeper/',views.contact_us_keeper_view,name='contact_us_keeper'),

]