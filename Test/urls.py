from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='index'),
    path("register/", views.RegisterAPI.as_view(), name='register'),
    path("login/", views.LoginAPI.as_view(), name='login')
]