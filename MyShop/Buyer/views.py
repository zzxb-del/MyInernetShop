from django.shortcuts import render,HttpResponseRedirect
from Seller.views import setPassword
from Seller.models import *

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
    return render(request,"buyer/index.html",locals())


# Create your views here.
