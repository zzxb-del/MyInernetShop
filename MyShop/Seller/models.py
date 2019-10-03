from django.db import models

class Login_User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length = 32)

    username = models.CharField(max_length = 32,null = True,blank = True)
    phone_number = models.CharField(max_length = 11,null = True,blank = True)
    photo = models.ImageField(upload_to = "images",default="images/jbh.jpg")
    age = models.IntegerField(null = True,blank = True)
    gender = models.CharField(max_length = 32,null = True,blank = True)
    address = models.TextField(null = True,blank = True)
    user_type = models.IntegerField(default = 0 ) #买家0 卖家1 管理员2

class Vaild_Code(models.Model):
    code_content = models.CharField(max_length=32)
    code_user = models.EmailField()
    code_time = models.DateTimeField(auto_now=True)
    code_state = models.IntegerField(default=0)


class GoodsType(models.Model):
    type_label = models.CharField(max_length=32)
    type_description = models.TextField()
    type_picture = models.ImageField(upload_to="seller/images")

class Goods(models.Model):
    goods_number = models.CharField(max_length=11)
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    goods_count = models.IntegerField()
    goods_location = models.CharField(max_length=32)
    goods_safe_date = models.IntegerField()
    goods_pro_time = models.DateField(auto_now=True)
    goods_status = models.IntegerField()

    goods_description = models.TextField(default="好吃还不贵，快来抢购！！！")
    picture = models.ImageField(upload_to='images')
    goods_type = models.ForeignKey(to = GoodsType,on_delete=models.CASCADE,default=1)
    goods_store = models.ForeignKey(to = Login_User,on_delete=models.CASCADE,default=1)

# Create your models here.

