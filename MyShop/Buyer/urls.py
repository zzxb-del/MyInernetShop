from django.contrib import admin
from django.urls import path
from Buyer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path("login/",login),
    path("index/",index),
    path("logout/", logout),
]