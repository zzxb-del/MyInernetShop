
from django.shortcuts import render,HttpResponseRedirect
from Seller.models import *
import hashlib



def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def register(request):
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = Login_User.objects.filter(email = email).first()
            if not user:
                register_user = Login_User()
                register_user.email = email
                register_user.username = email
                register_user.password = setPassword(password)
                register_user.save()
            else:
                error_message = "邮箱已被注册，请登录"
        else:
            error_message = "邮箱不可为空"
    return render(request, "seller/register.html", locals())

def login(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = Login_User.objects.filter(email=email).first()
            if user:
                db_password = user.password
                password = setPassword(password)
                if db_password == password:
                    response = HttpResponseRedirect("/Seller/index")
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
    return render(request,"seller/login.html",locals())


def logout(request):
    response = HttpResponseRedirect("/Seller/login/")
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session["username"]
    return response

def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie_username = request.COOKIES.get("username")
        session_username = request.session.get("username")
        if cookie_username and session_username == cookie_username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Seller/login/")
    return inner

@loginValid
def index(request):
    return render(request, "seller/index.html", locals())

def base(request):
    return render(request, "seller/base.html", locals())

# Create your views here.
