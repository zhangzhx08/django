from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import aggregates, F
from django.core.cache import cache

from .models import *
from df_user.views import authenticated


@authenticated
def cart(request):
    """
    功能：购物车页面
    :param request: 默认request参数
    :return: 购物车页面
    """
    # 获取用户id，构建查询集
    user_id = request.session.get('user_id')
    cart_list = CartInfo.objects.filter(user_id=user_id).order_by('-pk')
    # 迫使查询集执行数据库查询，并产生查询集缓存，避免重复执行数据库查询
    bool(cart_list)
    length = len(cart_list)
    context = {'font_flag': 'cart', 'cart_list': cart_list, 'length': length}
    return render(request, 'df_cart/cart.html', context)


def cart_count(request):
    """
    功能：查询购物车商品数量，处理ajax请求
    :param request: 默认request参数
    :return: JsonReponse对象
    """
    user_id = request.session.get('user_id')        # QueryDict对象的get方法的默认返回值为None
    if user_id:
        if 'count' in request.COOKIES:
            count = request.COOKIES['count']
            return JsonResponse({'count': count})
        else:
            count = CartInfo.objects.filter(user_id=int(user_id)).count()
            resp = JsonResponse({'count': count})
            resp.set_cookie('count', count)
            return resp
    else:
        return JsonResponse({'count': 0})


def cart_add(request, gid, count):
    """
    功能：添加商品到购物车
    :param request: 默认request参数
    :param gid: 商品id
    :param count: 商品的数量
    :return: JsonReponse对象
    """
    # 检测用户未登录，设置COOKIES['HTTP_REFERER']，保存request.META['HTTP_REFERER']中的原页面地址
    if not request.session.get('user_id'):
        resp = JsonResponse({'authenticated': False})
        resp.set_cookie('HTTP_REFERER', request.META.get('HTTP_REFERER'))
        return resp
    else:
        # 将获取的参数转化为int类型
        gid = int(gid)
        count = int(count)
        # 获取用户id，
        user_id = int(request.session.get('user_id'))
        # 依据user_id查询用户购物车列表,并求得列表中元素的个数，尝试进一步根据goods_id获取指定cart
        cart_list = CartInfo.objects.filter(user_id=user_id)
        carts = cart_list.filter(goods_id=gid)
        length = len(cart_list)
        # 若商品已存在，则对其count属性进行维护,并返回商品类别的个数
        if bool(carts):
            carts.update(count=F('count')+count)
            return JsonResponse({'authenticated': True, 'cart_count': length})
        else:
            # 若商品不在用户购物车列表中，则新建Cart对象，赋值并保存
            cart = CartInfo(user_id=user_id, goods_id=gid, count=count)
            cart.save()
            # 构造JsonResponse对象，并设置COOKIES
            resp = JsonResponse({'authenticated': True, 'cart_count': length + 1})
            resp.set_cookie('count', length+1)
            return resp


# 购物车商品编辑
def cart_edit_count(request, gid, count):
    user_id = int(request.session['user_id'])
    cart = CartInfo.objects.get(user_id=user_id, goods_id=int(gid))
    cart.count = int(count)
    cart.save()
    return JsonResponse({'is_succeed': True})


# 维护购物车商品是否被选中
def cart_edit_status(request, gid, is_selected):
    user_id = int(request.session['user_id'])
    if gid == '00':
        if is_selected == '1':
            carts = CartInfo.objects.filter(user_id=user_id, is_selected=False)
            for cart in carts:
                cart.is_selected = True
                cart.save()
        else:
            carts = CartInfo.objects.filter(user_id=user_id, is_selected=True)
            for cart in carts:
                cart.is_selected = False
                cart.save()
        return JsonResponse({'is_succeed': True})
    else:
        cart = CartInfo.objects.get(user_id=user_id, goods_id=int(gid))
        if is_selected == '1':
            cart.is_selected = True
        else:
            cart.is_selected = False
        cart.save()
        return JsonResponse({'is_succeed': True})

# def cart_edit_status(request):
#     if request.GET.get('check_all') == 'true':
#         if request.GET.get('status') == 'true':
#             cart_list = CartInfo.objects.filter(is_selected=False)
#             for cart in cart_list:
#                 cart.is_selected = True
#                 cart.save()
#         else:
#             cart_list = CartInfo.objects.filter(is_selected=True)
#             for cart in cart_list:
#                 cart.is_selected = False
#                 cart.save()
#     else:
#         cart = CartInfo.objects.get(goods_id=request.GET.get('goods_id'))
#         if request.GET.get('status') == 'true':
#             cart.is_selected = True
#         else:
#             cart.is_selected = False
#         cart.save()
#     return JsonResponse({})


# 从购物车删除商品
def cart_delete(request, gid):
    user_id = request.session['user_id']
    cart = CartInfo.objects.get(user_id=user_id, goods_id=int(gid))
    cart.delete()
    # count = request.COOKIES['count']
    resp = JsonResponse({'is_delete': True})
    # resp.set_cookie('count', int(count)-1)
    return resp

