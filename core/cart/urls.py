from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('cart/',views.cart_view,name='cart'),
    path('add_to_cart/',views.add_to_cart_view,name='add_to_cart'),
    path('change_orderitem_count/',views.change_orderitem_count_view,name='change_orderitem_count'),
    path('remove_from_cart/',views.remove_from_cart_view,name='remove_from_cart'),
    path('confirm_order/',views.confirm_order_view,name='confirm_order'),
    path('user_recipient/',views.user_recipient_ajax,name='user_recipient'),
    path('check_confirm_order/',views.check_confirm_order_view,name='check_confirm_order'),
    path('shopping_payment/',views.shopping_payment_view,name='shopping_payment'),
    path('successful_payment/',views.successful_payment_view,name='successful_payment'),
    path('unsuccessful_payment/',views.unsuccessful_payment_view,name='unsuccessful_payment'),


]
