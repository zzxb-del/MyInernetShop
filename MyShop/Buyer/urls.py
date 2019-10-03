from django.contrib import admin
from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path("login/",login),
    path("index/",index),
    path("logout/", logout),
    path("goods_list/",goods_list),
    re_path('detail/(?P<id>\d+)/',detail),
    path("add_cart/", add_cart),
    path("cart/", cart),
    path("pay_order/", pay_order),
    path("pay_order_more/", pay_order_more),
    path("alipay/", AlipayViews),
    path("pay_result/", pay_result),

]