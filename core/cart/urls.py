from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('cart/',views.cart_view,name='cart'),
    path('add_to_cart/',views.add_to_cart_view,name='add_to_cart'),

]
