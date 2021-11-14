from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

from django.db.models.fields import related


def goods_images_name(instance, filename:str) -> str:
    return f'goods_images/{str(uuid4())}.{filename.split(".")[-1]}'


def category_images_name(instance, filename:str) -> str:
    return f'category_images/{str(uuid4())}.{filename.split(".")[-1]}'


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.FileField(upload_to=category_images_name)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"


class GoodsImages(models.Model):
    image = models.FileField(upload_to=goods_images_name)


class GoodsRequestImages(models.Model):
    image = models.FileField(upload_to=goods_images_name)


class Goods(models.Model):
    name = models.CharField(max_length=64)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goods")
    images = models.ManyToManyField(GoodsImages)
    description = models.CharField(max_length=1024)
    categories = models.ManyToManyField(Category, related_name="goods")
    price_s = models.DecimalField(max_digits=51, decimal_places=2)
    price_m = models.DecimalField(max_digits=51, decimal_places=2)
    price_l = models.DecimalField(max_digits=51, decimal_places=2)
    price_r = models.DecimalField(max_digits=51, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name} {self.provider}"

    class Meta:
        verbose_name_plural = "Goods"


class GoodsRequest(models.Model):
    name = models.CharField(max_length=64)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goods_requests")
    images = models.ManyToManyField(GoodsRequestImages)
    description = models.CharField(max_length=1024)
    categories = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=51, decimal_places=2)
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} {self.requester}"

    class Meta:
        verbose_name_plural = "Goods Requests"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    goods = models.ManyToManyField(Goods, related_name="orders",
                                   through_fields=('order_id', 'goods_id'), through='GoodsOrder')

    def __str__(self) -> str:
        return f"{self.customer.username} {self.id}"


class GoodsOrder(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='+')
    goods_id = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='+')


class Review(models.Model):
    author = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, related_name="reviews", on_delete=models.CASCADE)
    head = models.CharField(max_length=255)
    body = models.CharField(max_length=1024)
    rate = models.IntegerField()
