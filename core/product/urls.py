from django.urls import path 
from . import views

urlpatterns = [
    path('product/<int:id>/',views.detail_view,name='detail-view'),
]