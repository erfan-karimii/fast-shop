from django.urls import path 
from . import views 

app_name = 'account' 

urlpatterns = [
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('check_login/',views.check_login_view,name="check_login"),
    path('welcome/',views.welcome_page_view,name="welcome"),

]