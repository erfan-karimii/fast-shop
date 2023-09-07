from django.urls import path 
from . import views 

app_name = 'account' 

urlpatterns = [
    #login,logoy,register
    path('login/',views.login_view,name="login"),
    path('check_login/',views.check_login_view,name="check_login"),
    path('logout/',views.logout_view,name="logout"),
    path('register/',views.register_view,name="register"),
    path('check_register/',views.check_register_view,name="check_register"),
    path('reset_password/',views.reset_password_view,name="reset_password"),
    path('check_reset_password/',views.check_reset_password_view,name="check_reset_password"),
    path('welcome/',views.welcome_page_view,name="welcome"),

    #profile
    path('profile/',views.profile_view,name="profile"),
    path('sidebar/',views.sidebar_view,name="sidebar"),
    path('profile_edit/',views.profile_edit_view,name="profile_edit"),
    path('check_profile_edit/',views.check_profile_edit_view,name="check_profile_edit"),
    path('current_order/',views.current_order_view,name="current_order"),
    path('message_page/',views.message_page_view,name="message_page"),

]