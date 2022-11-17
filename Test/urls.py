from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='index'),
    path("v1/register/", views.RegisterAPI.as_view(), name='register'),
    path("v1/login/", views.LoginAPI.as_view(), name='login')
]