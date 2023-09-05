from django.urls import path 
from . import views

app_name = 'product'

urlpatterns = [
    path('product/<int:id>/',views.detail_view,name='detail-view'),
    path('list/',views.list_view,name='list-view'),
    path('list/category/<int:cat_id>/',views.list_view,name='list-cat-view'),
    path('validate_comment/',views.validate_comment_view,name='validate-comment'),
    path('wishlist/',views.wishlist_view,name='wishlist'),
    path('remove_from_wishlist/<int:id>/',views.remove_from_wishlist_view,name='remove_from_wishlist'),

    path('add_to_wishlist/',views.add_to_wishlist_ajax,name='add-to-wishlist'),


]