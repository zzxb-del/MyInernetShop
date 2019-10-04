from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse
from Seller.views import setPassword
from Seller.models import *
from Buyer.models import *

def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie_username = request.COOKIES.get("username")
        session_username = request.session.get("username")
        if cookie_username and session_username and cookie_username == session_username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

def register(request):
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        if email:
            user = Login_User.objects.filter(email = email).first()
            if not user:
                register_user = Login_User()
                register_user.email = email
                register_user.username = username
                register_user.password = setPassword(password)
                register_user.save()
            else:
                error_message = "用户不存在"
        else:
            error_message = "邮箱不可为空"
        return HttpResponseRedirect("/Buyer/login/")
    return render(request,"buyer/register.html",locals())

from django.views.decorators.cache import cache_page
@cache_page(60*15) #使用缓存，缓存的寿命15分钟
def login(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        if email:
            user = Login_User.objects.filter(email=email).first()
            if user:
                db_password = user.password
                password = setPassword(password)
                if db_password == password:
                    response = HttpResponseRedirect("/Buyer/index")
                    response.set_cookie("username",user.username)
                    response.set_cookie("id",user.id)
                    request.session["username"] = user.username
                    return response
                else:
                    error_message = "密码错误"
            else:
                error_message = "用户不存在"
        else:
            error_message = "邮箱不可为空"
    return render(request,"buyer/login.html",locals())


def logout(request):
    url = request.META.get("HTTP_REFERER", "/Buyer/index/")
    response = HttpResponseRedirect(url)
    for k in request.COOKIES:
        response.delete_cookie(k)
    del request.session["username"]
    return response


def index(request):
    goods_type = GoodsType.objects.all()
    result = []
    for ty in goods_type:
        goods =  ty.goods_set.order_by("-goods_pro_time")
        if len(goods)>=4:
            goods = goods[:4]
            result.append({"type":ty,"goods_list":goods})
    return render(request,"buyer/index.html",locals())

def goods_list(request):
    request_type = request.GET.get('type')
    keyword = request.GET.get('keywords')
    goods_list = []
    if request_type == "t":  # t类型查询
        if keyword:
            id = int(keyword)
            goods_type = GoodsType.objects.get(id=id)  # 先查询类型
            goods_list = goods_type.goods_set.order_by("-goods_pro_time")  #再查询类型对应的商品)
    elif request_type == 'k':
        if keyword:
            goods_list = Goods.objects.filter(goods_name__contains=keyword).order_by('-goods_pro_time')
    if goods_list:
        lenth = len(goods_list)/5
        if lenth != int(lenth):
            lenth += 1
        lenth = int(lenth)
        recommend = goods_list[:lenth]

    return render(request,"buyer/goods_list.html",locals())

def detail(request,id):
    goods = Goods.objects.get(id = int(id))
    return render(request,"buyer/detail.html",locals())

def add_cart(request):
    result = {
        "code": 200,
        "data": ""
    }
    if request.method == 'POST':
        id = int(request.POST.get("goods_id"))
        count = int(request.POST.get("count",1))

        goods = Goods.objects.get(id = id )
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_number = count
        cart.goods_price = goods.goods_price
        cart.goods_picture = goods.picture
        cart.goods_total = goods.goods_price * count
        cart.goods_id = id
        cart.cart_user = request.COOKIES.get("id")
        cart.save()
        result["data"] = "加入购物车成功"
    else:
        result["code"] = 500
        result["data"] = "请求方式错误"
    return JsonResponse(result)

def cart(request):
    """返回当前用户购物车当中的商品以-id"""
    user_id = request.COOKIES.get("id")
    goods = Cart.objects.filter(cart_user = int(user_id)).order_by("-id")
    count = goods.count()
    return render(request,"buyer/cart.html",locals())


import datetime
import time

@loginValid
def pay_order_more(request):
    data = request.GET
    print(data)
    data_item = data.items()
    request_data = []
    for key,value in data_item:
        if key.startswith("check_"):
            goods_id = key.split("_",1)[1]
            count = data.get("count_"+goods_id)
            request_data.append((int(goods_id),int(count)))
    print(request_data)
    if request_data:
        #保存订单表，但是保存总价
        order = PayOrder()
        order.order_number = str(time.time()).replace(".","")
        order.order_data = datetime.datetime.now()
        order.order_status = 0
        order.order_user = Login_User.objects.get(id = int(request.COOKIES.get("id"))) #订单对应的买家
        order.save()
        #保存订单详情
        #查询商品的信息
        order_total = 0
        for goods_id,count in request_data:
            goods = Goods.objects.get(id = int(goods_id))
            order_info = OrderInfo()
            order_info.order_id = order
            order_info.goods_id = goods.id
            order_info.goods_picture = goods.picture
            order_info.goods_name = goods.goods_name
            order_info.goods_count = int(count)
            order_info.goods_price = goods.goods_price
            order_info.goods_total_price = goods.goods_price*int(count)
            order_info.store_id = goods.goods_store #商品卖家，goods.goods_store本身就是一条卖家数据
            order_info.save()
            order_total += order_info.goods_total_price #总价计算
        order.order_total = order_total
        order.save()
    return render(request,"buyer/pay_order.html",locals())


@loginValid
def pay_order(request):
    goods_id = request.GET.get("goods_id")
    count = request.GET.get("count")
    if goods_id and count:
        # 保存订单表，但是保存总价
        order = PayOrder()
        order.order_number = str(time.time()).replace(".", "")
        order.order_data = datetime.datetime.now()

        order.order_user = Login_User.objects.get(id=int(request.COOKIES.get("id")))  # 订单对应的买家
        order.save()
        # 保存订单详情
        # 查询商品的信息
        goods = Goods.objects.get(id=int(goods_id))
        order_info = OrderInfo()
        order_info.order_id = order
        order_info.goods_id = goods.id
        order_info.goods_picture = goods.picture
        order_info.goods_name = goods.goods_name
        order_info.goods_count = int(count)
        order_info.goods_price = goods.goods_price
        order_info.goods_total_price = goods.goods_price * int(count)
        order_info.store_id = goods.goods_store  # 商品卖家，goods.goods_store本身就是一条卖家数据
        order_info.save()
        order.order_total = order_info.goods_total_price
        order.save()
    return render(request,"buyer/pay_order.html",locals())

from MyShop.settings import alipay_public_key_string,alipay_private_key_string
from alipay import  AliPay

def AlipayViews(request):
    order_number = request.GET.get("order_number")
    order_total = request.GET.get("total")
    alipay = AliPay(
        appid = "2016101200667724",
        app_notify_url = None,
        app_private_key_string = alipay_private_key_string,
        alipay_public_key_string = alipay_public_key_string,
        sign_type = "RSA2"
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_number,
        total_amount = str(order_total),
        subject = "来自北京的雾霾",
        return_url = "http://127.0.0.1:8000/Buyer/pay_result/",
        notify_url = "http://127.0.0.1:8000/Buyer/pay_result/"
    )
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)

def pay_result(request):
    out_trade_no = request.GET.get("out_trade_no")
    if out_trade_no:
        order = PayOrder.objects.get(order_number = out_trade_no)
        order.orderinfo_set.all().update(order_status = 1)
    return render(request,"buyer/pay_result.html",locals())

@loginValid
def user_center_info(request):
    return render(request,"buyer/user_center_info.html",locals())

@loginValid
def user_center_order(request):
    user_id = request.COOKIES.get("id")
    user = Login_User.objects.get(id = int(user_id))
    order_list = user.payorder_set.order_by("-order_data")
    return render(request,"buyer/user_center_order.html",locals())


# Create your views here.
