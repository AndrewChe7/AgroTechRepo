from django.contrib import admin
from . import models

# Register your models here.

class GoodsOrderInline(admin.TabularInline):
    model = models.goods_order
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines=(GoodsOrderInline,)

class GoodsAdmin(admin.ModelAdmin):
    inlines=(GoodsOrderInline,)

admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.goods_images)
admin.site.register(models.Review)