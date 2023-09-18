from  django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('chat/<str:username>',views.chatPage,name='chat'),
    path('search/', views.account_search_view, name='search'),

  
]