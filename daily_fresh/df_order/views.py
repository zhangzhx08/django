from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import request, HttpResponse, JsonResponse
from django.db import transaction
from .models import *
from df_cart.models import *
from df_user.models import *
from df_user.views import is_login
from datetime import datetime


@is_login
def place_order(request):
    site = UserInfo.objects.get(id=request.session.get('user_id')).siteinfo_set.get(is_default=True)
    cart_list = CartInfo.objects.filter(is_selected=True)
    length = len(cart_list)
    # 取反速度比排序快，建议用取反
    # index_list.sort(reverse=True)
    index_list = [x for x in range(1, len(cart_list)+1)][::-1]
    context = {
        'font_flag': 'place_order',
        'cart_list': cart_list,
        'index_list': index_list,
        'site': site,
        'length': length,
    }
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
def order_haddle(request):
    sid = transaction.savepoint()
    try:
        cart_list = CartInfo.objects.filter(is_selected=True)
        length = len(cart_list)
        user = cart_list[0].user
        totle = 0
        # 判断库存是否足够，计算总价,相应商品库存量扣除
        for cart in cart_list:
            if cart.count < cart.goods.ginventory:
                totle += cart.goods.gprice*cart.count
                cart.goods.ginventory -= cart.count
                cart.goods.save()
            else:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'is_succeed': False, 'inventory': True, 'except': False})
        # 创建订单对象
        order = OrderInfo()
        order.user_id = request.session.get('user_id')
        order.ototle = totle
        order.odate = datetime.now()
        order.oaddress = request.POST.get('address')
        order.save()
        # 创建订单详情对象,并删除购物车商品
        for cart in cart_list:
            order_detail = OrderDetailInfo()
            order_detail.goods = cart.goods
            order_detail.ocount = cart.count
            order_detail.order = order
            order_detail.save()
            cart.delete()
        transaction.savepoint_commit(sid)
        resp = JsonResponse({'is_succeed': True, 'inventory': False, 'except': False})
        resp.set_cookie('count', int(request.COOKIES.get('count'))-length)
        return resp

    except Exception as e:
        print(e)
        transaction.savepoint_rollback(sid)
        return JsonResponse({'is_succeed': False, 'inventory': False, 'except': True})


