from django.contrib import admin
from django.urls import path,re_path
from Seller.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path("login/",login),
    path("logout/",logout),
    path("index/",index),
    path('slc/', send_login_code),
    path("person_info/",person_info),
    path("goods_add/",goods_add),
    re_path(r'goods_list/(?P<page>\d+)/(?P<status>[01])/', goods_list),
    re_path(r'goods_status/(?P<state>\w+)/(?P<id>\d+)/', goods_status),
]