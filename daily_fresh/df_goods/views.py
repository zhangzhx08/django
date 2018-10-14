# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.core.cache import cache
from django.db.models import F
from .models import *


# @cache_page(10)
# @vary_on_cookie
def index(request):
    """
    功能：商城主页视图
    :param request: 默认request参数
    :return: 商城主页
    """
    # 获取商品种类查询集
    categorys = Category.objects.filter(is_delete=False)
    # 获取个种类的点击量前四个，以及最新添加的两个，使用insert(0,value)是为了在模板中使用list.pop方法
    list_by_click = []
    list_by_pk = []
    for category in categorys:
        list_by_click.insert(0, category.goodsinfo_set.order_by('-gclick')[0:4])
        list_by_pk.insert(0, category.goodsinfo_set.order_by('-pk')[0:2])
    # 构造模板上下文
    context = {'font_flag': 'goods',
               'categorys': categorys,
               'list_by_click': list_by_click,
               'list_by_pk': list_by_pk,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, cid, type, index):
    """
    功能：天天生鲜具体商品种类的商品列表
    :param request: 默认的request参数
    :param cid: 商品种类id
    :param type: 商品列表排序依据
    :param index: 页码
    :return: 特定种类商品列表页
    """
    # 从缓存获取分类查询集，传递给分类表，如果没有，则查询数据库并缓存
    categorys = cache.get('categorys')
    if not categorys:
        categorys = Category.objects.filter(is_delete=False)
        cache.set('categorys', categorys, 3600)
    # 从缓存获取当前分类中最新的2个商品，如果没有，则查询数据库并缓存结果
    cate00 = cache.get('category_new_goods:'+cid)
    if not cate00:
        category = categorys.get(pk=int(cid))
        cate00 = category.goodsinfo_set.filter(is_delete=False).order_by('-pk')[0:2]
        cache.set('category_new_good:'+cid, cate00, 300)
    # 从缓存中获取当前分类所有商品按制定方式排序的查询集的Paginator分页对象，如果没有，则查询数据库并缓存
    paginator = cache.get('category_goods_list_paginator:'+cid+type)
    if not paginator:
        if type == 'default':
            goods_list = category.goodsinfo_set.filter(is_delete=False).order_by('-gclick')
        elif type == 'price':
            goods_list = category.goodsinfo_set.filter(is_delete=False).order_by('-gprice')
        else:
            goods_list = category.goodsinfo_set.filter(is_delete=False).order_by('-gsales')
        # 查询集分页
        paginator = Paginator(goods_list, 10)
        # 缓存结果
        cache.set('category_goods_list_paginator:'+cid+type, paginator, 300)
    # 获取用户 请求的页
    page = paginator.page(int(index))
    # 构造Json数据
    context = {
        'font_flag': 'goods',
        'categorys': categorys,
        'category': category,
        'type': type,
        'page': page,
        'cate00': cate00
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    """
    功能：商品详情页视图
    :param request: 默认request参数
    :param gid: 商品id
    :return: 商品详情页
    """
    # 从缓存获取分类查询集，传递给分类表，如果没有，则查询数据库并缓存
    categorys = cache.get('categorys')
    if not categorys:
        categorys = Category.objects.filter(is_delete=False)
        cache.set('categorys', categorys, 3600)
    # 获取商品对象，维护商品点击量:加1
    goods = cache.get('goods:'+gid)
    if not goods:
        goods = GoodsInfo.objects.get(pk=str(gid))
        cache.set('goods:'+gid, goods, 300)
    # 维护点击量的任务应该交给celery去做，从缓存中得到的goods无法维护点击量
    goods.gclick += 1
    goods.save()
    # 可以使用QuerySet.update()方法结合F对象更改数据库的数值，但是不太实用，直接使用对象更改并save更简洁
    # goods_queryset = GoodsInfo.objects.filter(pk=int(gid))
    # goods_queryset[0].update(gclick=F('gclick')+1)

    # 获取COOKIES,维护最近浏览商品的id
    cookie = request.COOKIES
    browsed_goods_id_list = []
    # 如果COOKIES中存在键：‘browsed_goods_id_list’，则对对应的value切片处理
    if 'browsed_goods_id_list' in cookie:
        browsed_goods_id_list = cookie['browsed_goods_id_list'].split('|')
    # 将商品id写入列表
    try:
        browsed_goods_id_list.remove(gid)
    except Exception:
        pass
    browsed_goods_id_list.insert(0, gid)
    # 若切片所得列表长度是否大于等于5，将最后一个删除
    if len(browsed_goods_id_list) > 5:
        browsed_goods_id_list.pop()

    # 从缓存获取当前分类中最新的2个商品，如果没有，则查询数据库并缓存结果
    category = goods.category
    cid = category.id
    cate00 = cache.get('category_new_goods:'+str(cid))
    if not cate00:
        category = categorys.get(pk=cid)
        cate00 = category.goodsinfo_set.filter(is_delete=False).order_by('-pk')[0:2]
        cache.set('category_new_good:'+str(cid), cate00, 300)
    # 构造模板上下文
    context = {
        'font_flag': 'goods',
        'categorys': categorys,
        'category': category,
        'goods': goods,
        'cate00': cate00
    }
    # 构造渲染页面
    resp = render(request, 'df_goods/detail.html', context)
    # 将商品id列表以'|'为分隔符，组成id字符串,写入COOKIES
    resp.set_cookie('browsed_goods_id_list', '|'.join(browsed_goods_id_list))
    return resp
