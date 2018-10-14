# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import *
from df_order.models import *
from df_goods.models import *
from hashlib import sha1
from functools import wraps
from django.contrib.sessions import base_session


def register(request):
    """
    功能：用户注册页面
    :param request: 默认request参数
    :return: 用户注册页面
    """
    cookie = request.COOKIES
    name = cookie.get('regi_uname', '')
    email = cookie.get('regi_uemail', '')
    context = {'regi_name': name, 'regi_email': email}
    return render(request, 'df_user/register.html', context)


def register_exist(request):
    """
    功能：判断用户名是否存在，处理ajax请求
    :param request: 默认request参数
    :return: JsonResponse对象
    """
    # 获取用户输入的用户名，查询数据库是否存在该用户名
    uname = request.GET.get('regi_name')
    result = UserInfo.objects.filter(uname=uname).exists()
    context = {'result': result}
    return JsonResponse(context)


def register_handle(request):
    """
    功能：用户名注册处理，处理post请求
    :param request: 默认request参数
    :return: 重定向到登录页面或注册页面
    """
    # 获取提交的用户名、密码
    post = request.POST
    uname = post.get('user_name')
    pwd = post.get('pwd')
    # 判断两次密码是否相同、用户名是否存在
    if post.get('pwd') != post.get('cpwd') or UserInfo.objects.filter(uname=uname).exists():
        # 获取重定向页面
        red = redirect(reverse('df_user:register'))
        # 设置COOKIES
        red.set_cookie('regi_name', post.get('user_name'), max_age=300)
        red.set_cookie('regi_email', post.get('email'), max_age=300)
        return red
    else:
        # 使用sha1进行密码加密
        s1 = sha1()
        s1.update(pwd.encode())
        upwd = s1.hexdigest()
        # 创建UserInfo对象，赋值并保存
        user = UserInfo()
        user.uname = uname
        user.upwd = upwd
        user.uemail = post.get('email')
        user.save()
        return redirect(reverse('df_user:login', args=()))


def login(request):
    """
    功能：登录页面
    :param request: 默认request参数
    :return: 登录页面
    """
    # 打印request.META中的键值对内容
    # for item in request.META:
    #     print(item+'======', end='')
    #     print(request.META[item])
    # 尝试获取COOKIES中保存的uname，如果以前登录并记录过用户名，则直接显示用户名
    uname = request.COOKIES.get('uname', '')
    context = {'uname': uname, 'error_name': 0, 'error_pwd': 0}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    """
    功能：登陆处理
    :param request: 默认request参数
    :return:
    """
    # 获取POST属性
    post = request.POST
    # 获取post中的value值
    uname = post.get('user_name')
    upwd = post.get('pwd')
    remember = post.get('remember', '0')
    # 获取uname的查询集
    users = UserInfo.objects.filter(uname=uname)
    # 判断用户名是否存在
    if bool(users):
        # 密码加密处理
        s = sha1()
        s.update(upwd.encode())
        upwd_sha = s.hexdigest()
        # 判断密码是否正确
        if upwd_sha == users[0].upwd:
            # 尝试获取跳转前的原页面url(未登录状态下点击添加购物车)
            if 'HTTP_REFERER' in request.COOKIES:
                url = request.COOKIES.get('HTTP_REFERER')
            # 若无法获取到原页面url，则尝试获取跳转前想要请求的页面，default值设置为首页url
            else:
                url = request.COOKIES.get('request_url', reverse('df_goods:index'))
            # 构造HttpResponseRedirect对象
            red = redirect(url)
            # 删除COOKIES['HTTP_REFERER']中保存的跳转前的原页面地址、跳转前想要请求的地址
            red.delete_cookie('HTTP_REFERER')
            red.delete_cookie('request_url')

            # 设置cookie，记住用户名
            if remember == '1':
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            # 设置session内容及过期时间(可在setting文件中配置)，状态保持
            request.session['user'] = users[0]
            request.session['user_id'] = users[0].id
            request.session['uname'] = uname
            # request.session.set_expiry(7200)
            return red
        else:
            # 构造HttpResponseRedirect对象
            red = redirect(reverse('df_user:login'))
            # 设置cookie，记住用户名
            if remember == '1':
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            red.set_cookie('error_name', 0)
            red.set_cookie('error_pwd', 1)
            return red
    else:
        # 构造HttpResponseRedirect对象
        red = redirect(reverse('df_user:login'))
        # 设置cookie，记住用户名
        if remember == '1':
            red.set_cookie('uname', uname)
        else:
            red.set_cookie('uname', '', max_age=-1)
        red.set_cookie('error_name', 1)
        red.set_cookie('error_pwd', 0)
        return red


def authenticated(func):
    """
    功能：装饰器，用户登录状态认证
    :param func:
    :return:
    """
    @wraps(func)
    def inner_func(request, *args, **kwargs):
        """
        功能：扩充后的新函数
        :param request: 原函数的默认参数
        :param args: 原函数的位置参数，采用不定长参数形式来表示
        :param kwargs: 原函数的关键字参数，采用不定长参数形式来表示
        :return:
        """
        # 若已登录则继续执行原视图
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        # 若未登录，则重定向到登录页面
        else:
            redi = redirect(reverse('df_user:login'))
            # 设置cookie保存原来的页面地址
            redi.set_cookie('request_url', request.get_full_path())
            return redi
    return inner_func


def logout(request):
    """
    功能：删除session，退出登录，重定向到首页
    :param request: 默认request参数
    :return: 首页
    """
    # 删除session
    request.session.flush()
    # 获取重定向页面
    resp = redirect(reverse('df_goods:index'))
    # 删除COOKIES中记录购物车商品数量的键：count
    resp.delete_cookie('count')
    return resp


@authenticated
def user_center_info(request):
    """
    功能：用户中心页面
    :param request: 默认request参数
    :return: 用户中心页面
    """
    # 根据session保存的user_id获取user对象,以及相关信息
    user = request.session.get('user')
    # 获取最近浏览商品id列表
    id_list_str = request.COOKIES.get('browsed_goods_id_list')
    id_list = []
    goods_list = []
    if id_list_str:
        id_list = id_list_str.split(',')
    for id in id_list:
        goods_list.append(GoodsInfo.objects.get(pk=id))
    # 构造Json数据
    context = {
        'font_flag': 'user_center',
        'uname': user.uname,
        'uemail': user.uemail,
        'uphone': user.uphone,
        'uaddress': user.uaddress,
        'goods_list': goods_list,
    }
    return render(request, 'df_user/user_center_info.html', context)


@authenticated
def user_center_order(request, index):
    """
    功能：用户中心---订单列表页面
    :param request: 默认request参数
    :param index: 订单页页码
    :return: 订单列表页面
    """
    # 获取用户id；并尝试从缓存中获取Paginator对象
    user_id = request.session['user_id']
    paginator = cache.get('order_list_paginator:'+str(user_id))
    # 如果缓存中没有（即返回None），则查询数据库；对QuerySet分页；并将Paginator对象缓存至数据库；
    if not paginator:
        order_list = OrderInfo.objects.filter(user_id=user_id, is_pay=False).order_by('-pk')
        paginator = Paginator(order_list, 8)
        cache.set('order_list_paginator:'+str(user_id), paginator, 60*5)
    # 获取请求的页；构造模板上下文；返回结果
    page = paginator.page(int(index))
    context = {'font_flag': 'user_center', 'page': page}
    return render(request, 'df_user/user_center_order.html', context)


def site_haddle(request):
    """
    功能：添加收货地址
    :param request: 默认request参数
    :return:
    """
    post = request.POST
    site = SiteInfo()
    site.sperson = post.get('sperson')
    site.sphone = post.get('sphone')
    site.spostcode = post.get('spostcode')
    site.saddress = post.get('saddress')
    # 外键user的值必须是一个UserInfo对象，可直接使用user_id进行赋值操作
    site.user_id = request.session['user_id']
    site.save()
    return redirect(reverse('df_user:user_center_site'))


@authenticated
def user_center_site(request):
    """
    功能：用户中心---收货地址页面
    :param request: 默认request参数
    :return: 用户中心---收货地址页面
    """
    # 获取用户默认收货地址
    # 外键user的值必须是一个UserInfo对象，可直接使用user_id进行查询操作
    sites = SiteInfo.objects.filter(user_id=request.session['user_id'], is_default=True)
    site = sites[0]
    # 构建Json数据
    context = {
        'font_flag': 'user_center',
        'sperson': site.sperson,
        'sphone': site.sphone,
        'saddress': site.saddress,
        'spostcode': site.spostcode,
    }
    return render(request, 'df_user/user_center_site.html', context)
