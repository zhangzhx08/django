from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import request, HttpResponse, JsonResponse

from .models import *
from df_user.views import is_login


# 购物车
@is_login
def cart(request):
    user_id  = request.session.get('user_id')
    cart_list = CartInfo.objects.filter(user_id = user_id)
    length = len(cart_list)
    context = {'font_flag': 'cart', 'cart_list': cart_list, 'length': length}
    return render(request, 'df_cart/cart.html', context)


# 购物车商品数量显示
def cart_count(request):
    user_id = request.session.get('user_id', False)
    if user_id:
        if 'count' in request.COOKIES:
            count = request.COOKIES['count']
            return JsonResponse({'count': count})
        else:
            count = len(CartInfo.objects.filter(user_id=int(user_id)))
            resp = JsonResponse({'count': count})
            resp.set_cookie('count', count)
            return resp
    else:
        return JsonResponse({'count': 0})


# 添加商品到购物车
def cart_add(request, gid, count):
    # if reverse('df_cart:cart') in request.META['HTTP_REFERER']:
    # 检测用户未登录，设置COOKIES['HTTP_REFERER']，保存request.META['HTTP_REFERER']中的原页面地址
    if not request.session.get('user_id'):
        resp = JsonResponse({'is_login': False})
        resp.set_cookie('HTTP_REFERER', request.META.get('HTTP_REFERER'))
        return resp
    else:
        # 将获取的参数转化为int类型
        gid = int(gid)
        count = int(count)

        # 获取用户id，依据user_id查询用户购物车列表,并求得列表中元素的个数
        user_id = int(request.session.get('user_id'))
        cart_list = CartInfo.objects.filter(user_id=user_id)
        length = len(cart_list)
        # 遍历用户购物车列表，若商品已存在，则对其count属性进行维护,并返回商品类别的个数
        for item in cart_list:
            if item.goods_id == gid:
                item.count = item.count+count
                item.save()
                return JsonResponse({'is_login': True, 'cart_count': length})

        # 若商品不在用户购物车列表中，则新建Cart对象，赋值并保存
        cart = CartInfo()
        cart.user_id = user_id
        cart.goods_id = gid
        cart.count = count
        cart.save()
        return JsonResponse({'is_login': True, 'cart_count': length+1})


# 购物车商品编辑
def cart_edit(request, gid, count):
    cart = CartInfo.objects.get(goods_id=int(gid))
    cart.count = int(count)
    cart.save()
    return JsonResponse({'status': True})


# 从购物车删除商品
def cart_delete(request, gid):
    cart = CartInfo.objects.get(goods_id=int(gid))
    cart.delete()
    count = request.COOKIES['count']
    resp = JsonResponse({'is_delete': True})
    resp.set_cookie('count', int(count)-1)
    return resp

