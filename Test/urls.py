from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='index'),
    path("v1/register", views.RegisterAPI.as_view(), name='register'),
    path("v1/login", views.LoginAPI.as_view(), name='login'),
    path("v1/fileUpload", views.FileUploadAPI.as_view(), name='fileUpload'),
    path("v1/verification",views.EmailVerificationAPI.as_view(),name="verification")
]
