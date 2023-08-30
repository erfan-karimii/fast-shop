from django.urls import path 
from . import views

app_name = 'product'

urlpatterns = [
    path('product/<int:id>/',views.detail_view,name='detail-view'),
    path('validate_comment/',views.validate_comment,name='validate-comment'),

]