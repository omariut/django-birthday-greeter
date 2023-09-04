from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from django.urls import path

from users.views import UserCreateAPIView,UserListAPIView

urlpatterns = [
    path('registration', UserCreateAPIView.as_view(), name='user-registration-api'),
    path('users', UserListAPIView.as_view(),name='user-list'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'), 

]