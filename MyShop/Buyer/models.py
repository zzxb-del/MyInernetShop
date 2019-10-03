from django.db import models
class Cart(models.Model):
    '''商品名称
    商品数量（购买数量）
    商品价格
    商品图片
    商品总价（单个商品）
    商品id
    用户'''
    goods_name = models.CharField(max_length=32)
    goods_number = models.IntegerField()
    goods_price = models.FloatField()
    goods_picture = models.CharField(max_length=32)
    goods_total = models.FloatField()
    goods_id = models.IntegerField()
    cart_user = models.IntegerField()
# Create your models here.
