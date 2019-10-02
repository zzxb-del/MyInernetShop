from django.contrib import admin
from django.urls import path
from Seller.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path("login/",login),
    path("logout/",logout),
    path("index/",index),
]