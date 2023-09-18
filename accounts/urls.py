from .views import *
from django.urls import path,include

urlpatterns = [
    path('',index,name="index"),
    path('hello',hello,name="hello"),
    path('login' , login_attempt , name="login"),
    path('register' , register , name="register"),
    path('otp' , otp , name="otp"),
    path('login-otp', login_otp , name="login_otp") ,
    path('account/<int:user_id>/', account_view, name='account_view'),
    path('logout',logout,name='logout'),
    
]