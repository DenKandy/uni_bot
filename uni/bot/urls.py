from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path, include
from .views import RegisterUser

urlpatterns = [
    path(
        RegisterUser.URL, 
        RegisterUser.as_view(), 
        name=RegisterUser.NAME),
]