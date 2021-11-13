from django.db import models
from django.contrib.auth.models import User
from UserSystem import models as userSystemModels
from uuid import uuid4

# Create your models here.

class Goods(models.Model):
    name = models.CharField(max_length=64)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="providers")
    description = models.CharField(max_length=1024)
    price_s = models.DecimalField(max_digits=51, decimal_places=2)
    price_m = models.DecimalField(max_digits=51, decimal_places=2)
    price_l = models.DecimalField(max_digits=51, decimal_places=2)
    price_r = models.DecimalField(max_digits=51, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name} {self.provider}"

    class Meta:
        verbose_name_plural="Goods"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    goods = models.ManyToManyField(Goods, related_name="orders", through_fields=('order_id', 'goods_id'), through='goods_order')

    def __str__(self) -> str:
        return f"{self.customer.username} {self.id}"


class goods_order(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='+')
    goods_id = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='+')


def goods_images_name(instance, filename:str) -> str:
    return f'goods_images/{str(uuid4())}.{filename.split(".")[-1]}'


class goods_images(models.Model):
    goods_id = models.ForeignKey(Goods, related_name="image", on_delete=models.CASCADE)
    image = models.FileField(upload_to=goods_images_name)

    class Meta:
        verbose_name_plural="goods_images"


class Review(models.Model):
    author = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, related_name="reviews", on_delete=models.CASCADE)
    head = models.CharField(max_length=255)
    body = models.CharField(max_length=1024)
    rate = models.IntegerField()
