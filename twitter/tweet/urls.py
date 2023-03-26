
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('profiles',profiles,name='profiles'),
    path('profile/<int:pk>',profile,name='profile'),
   
    path('login',login_user,name='login'),
    path('logout',logout_user,name='logout'),
    path('register',register_user,name='register'),
    path('update_user/<int:pk>',update_user,name='update_user'),
]