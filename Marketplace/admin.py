from django.contrib import admin
from . import models


# Register your models here.
class GoodsOrderInline(admin.TabularInline):
    model = models.GoodsOrder
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (GoodsOrderInline,)


class GoodsAdmin(admin.ModelAdmin):
    inlines = (GoodsOrderInline, )


admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.GoodsImages)
admin.site.register(models.Review)
admin.site.register(models.Category)
admin.site.register(models.GoodsRequest)
