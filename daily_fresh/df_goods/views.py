# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from django.http import request, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from .models import *


def index(request):
    categorys = Category.objects.filter(is_delete=False)
    list_by_click = []
    list_by_pk = []
    # for index in range(0, len(categorys)):
    #     list_by_click.insert(0, categorys[index].goodsinfo_set.order_by('-gclick')[0:4])
    #     list_by_pk.insert(0, categorys[index].goodsinfo_set.order_by('-pk')[0:2])
    for category in categorys:
        list_by_click.append(category.goodsinfo_set.order_by('-gclick')[0:4])
        list_by_pk.append(category.goodsinfo_set.order_by('-pk')[0:2])
    list_by_click = list_by_click[::-1]
    list_by_pk = list_by_pk[::-1]

    context = {'font_flag': 'goods',
               'categorys': categorys,
               'list_by_click': list_by_click,
               'list_by_pk': list_by_pk,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, cid, type, index):
    # 获取分类查询集，传递给分类表
    categorys = Category.objects.filter(is_delete=False)
    # 获取当前分类的最新2个商品
    category = categorys.get(pk=int(cid))
    cate00 = category.goodsinfo_set.filter(is_delete=False).order_by('-pk')[0:2]
    # 获取当前分类中所有商品按制定方式排序的查询集
    goods_list = []
    if type == 'default':
        goods_list = category.goodsinfo_set.filter(is_delete=False).order_by('-gclick')
    elif type == 'price':
        goods_list = category.goodsinfo_set.filter(is_delete=False).order_by('-gprice')
    else:
        goods_list = category.goodsinfo_set.filter(is_delete=False).order_by('-gsales')

    # 分页
    paginator = Paginator(goods_list, 10)
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
    # 获取全部分类
    categorys = Category.objects.filter(is_delete=False)
    # 维护商品点击量:加1
    goods = GoodsInfo.objects.get(pk=int(gid))
    goods.gclick += 1
    goods.save()

    # 获取COOKIES,维护最近浏览商品的id
    cookie = request.COOKIES
    browsed_goods_id_list = []
    # 如果COOKIES中存在键：‘browsed_goods_id_list’，则对对应的value切片处理
    if 'browsed_goods_id_list' in cookie:
        browsed_goods_id_list = cookie['browsed_goods_id_list'].split(',')
    # 将商品id写入列表
    for id in browsed_goods_id_list:
        if id == gid:
            browsed_goods_id_list.remove(id)
            break
    browsed_goods_id_list.insert(0, str(gid))
    # 若切片所得列表长度是否大于等于5，将最后一个删除
    if len(browsed_goods_id_list) > 5:
        browsed_goods_id_list.pop()

    # 获取本分类中的两个新品
    category = goods.category
    cate00 = category.goodsinfo_set.filter(is_delete=False).order_by('-pk')[0:2]
    # 构造Json数据
    context = {
        'font_flag': 'goods',
        'categorys': categorys,
        'category': category,
        'goods': goods,
        'cate00': cate00
    }
    resp = render(request, 'df_goods/detail.html', context)
    # 将商品id列表以','为分隔符，组成id字符串,写入COOKIES
    resp.set_cookie('browsed_goods_id_list', ','.join(browsed_goods_id_list))
    return resp
