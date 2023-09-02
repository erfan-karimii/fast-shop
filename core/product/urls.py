from django.urls import path 
from . import views

app_name = 'product'

urlpatterns = [
    path('product/<int:id>/',views.detail_view,name='detail-view'),
    path('list/',views.list_view,name='list-view'),
    path('list/category/<int:cat_id>/',views.list_view,name='list-cat-view'),
    path('validate_comment/',views.validate_comment,name='validate-comment'),

]