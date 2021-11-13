from django.shortcuts import render, redirect
from Marketplace.models import Category, Goods, GoodsRequest
from UserSystem.models import UserTypes


# Create your views here.
def marketplace(request):
    return render(request, 'marketplace.html', context={
        'categories': Category.objects.all()
    })


def my_goods(request):
    if request.user.user_info.user_type == UserTypes.PROVIDER:
        goods = Goods.objects.filter(provider=request.user)
    elif (request.user.user_info.user_type == UserTypes.RETAIL_PURCHASER or
          request.user.user_info.user_type == UserTypes.WHOLESALE_PURCHASER):
        goods = GoodsRequest.objects.filter(requester=request.user)
    else:
        return redirect('/')
    return render(request, 'my_goods.html', {'goods': goods})


def category(request, category_id):
    try:
        category_object = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return redirect(404)
    if (request.user.user_info.user_type == UserTypes.RETAIL_PURCHASER or
            request.user.user_info.user_type == UserTypes.WHOLESALE_PURCHASER):
        goods = GoodsRequest.objects.filter(categories=category_object)
    elif request.user.user_info.user_type == UserTypes.PROVIDER:
        goods = Goods.objects.filter(categories=category_object)
    else:
        return redirect('/')
    return render(request, 'category.html', {'category': category_object, 'goods': goods})
