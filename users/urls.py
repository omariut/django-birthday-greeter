from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from django.urls import path

from users.views import (
    registration, 
    login, 

)
urlpatterns = [
    path('', registration, name='user-registration-api'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'), 

]