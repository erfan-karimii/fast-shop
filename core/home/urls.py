from django.urls import path 
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.home_view,name='home'),
    path('header/',views.header_view,name='header'),
    path('footer/',views.footer_view,name='footer'),

]