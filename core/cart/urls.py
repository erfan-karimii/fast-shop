from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('cart/',views.cart_view,name='cart'),
    path('add_to_cart/',views.add_to_cart_view,name='add_to_cart'),
    path('change_orderitem_count/',views.change_orderitem_count_view,name='change_orderitem_count'),
    path('remove_from_cart/',views.remove_from_cart_view,name='remove_from_cart'),

]
