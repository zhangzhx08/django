# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from .models import *
from django.http import request, HttpResponse, JsonResponse, response
from django.core.urlresolvers import reverse
from hashlib import sha1


# 用户注册
def register(request):
    cookie = request.COOKIES
    name = cookie.get('regi_uname', '')
    email = cookie.get('regi_uemail', '')
    context = {'regi_name': name, 'regi_email': email}
    return render(request, 'df_user/register.html', context)


# 判断用户名是否存在
def register_exist(request):
    uname = request.GET.get('regi_name')
    count = UserInfo.objects.filter(uname=uname).count()
    context = {'count': count}
    return JsonResponse(context)


# 用户名注册处理
def register_handle(request):
    post = request.POST
    pwd = post.get('pwd')

    if post.get('pwd')==post.get('cpwd'):
        user = UserInfo()
        # 使用sha1进行密码加密
        s1 = sha1()
        s1.update(pwd.encode())
        upwd = s1.hexdigest()

        user.uname = post.get('user_name')
        user.upwd = upwd
        user.uemail = post.get('email')
        user.save()
        return redirect(reverse('df_user:login', args=()))
    else:
        name = post.get('user_name')
        email = post.get('email')
        res = render(request, 'df_user/register.html')
        res.set_cookie('regi_name', name, max_age=300)
        res.set_cookie('regi_email', email, max_age=300)
        return res


# 登录
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'uname': uname, 'error_name': 0, 'error_pwd': 0}
    return render(request, 'df_user/login.html', context)


# 登录处理
def login_handle(request):
    # 获取POST属性
    post = request.POST
    # 获取post中的value值
    uname = post.get('user_name')
    upwd = post.get('pwd')
    remember = post.get('remember', '0')
    # 获取uname的查询集
    users = UserInfo.objects.filter(uname=uname)
    # 判断用户名是否存在
    if len(users) == 1:
        # 密码加密处理
        s = sha1()
        s.update(upwd.encode())
        upwd_sha = s.hexdigest()
        # 判断密码是否正确
        if upwd_sha == users[0].upwd:
            redi = redirect(reverse('df_user:user_center_info'))
            # 设置cookie，记住用户名
            if remember == '1':
                redi.set_cookie('uname', uname)
            else:
                redi.set_cookie('uname', '', max_age=-1)
            # 设置session，状态保持
            request.session['user_id'] = users[0].id
            request.session['uname'] = uname
            request.session.set_expiry(3600)
            return redi
        else:
            # 构造HttpResponseRedirect对象
            redi = redirect(reverse('df_user:login'))
            # 设置cookie，记住用户名
            redi.set_cookie('uname', uname)
            redi.set_cookie('error_name', 0)
            redi.set_cookie('error_pwd', 1)
            return redi
    else:
        # 构造HttpResponseRedirect对象
        redi = redirect(reverse('df_user:login'))
        # 设置cookie，记住用户名
        if remember == '1':
            redi.set_cookie('uname', uname)
        else:
            redi.set_cookie('uname', '')
        redi.set_cookie('error_name', 1)
        redi.set_cookie('error_pwd', 0)
        return redi


# 判断是否登录
def is_login(func):
    def login_func(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            redi = redirect(reverse('df_user:login'))
            redi.set_cookie('url', request.get_full_path)
            return redi
    return login_func


# 用户中心——用户信息
@is_login
def user_center_info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    uname = request.session['uname']
    uemail = user.uemail
    uphone = user.uphone
    uaddress = user.uaddress
    context = {'uemail': uemail, 'uname': uname, 'uphone': uphone, 'uaddress': uaddress, 'font_flag': 'user_center'}
    return render(request, 'df_user/user_center_info.html', context)


# 用户中心——用户订单
@is_login
def user_center_order(request):
    context = {'font_flag': 'user_center'}
    return render(request, 'df_user/user_center_order.html', context)


def site_haddle(request):
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



# 用户中西——收货地址
@is_login
def user_center_site(request):
    # 获取用户默认收货地址
    # 外键user的值必须是一个UserInfo对象，可直接使用user_id进行查询操作
    sites = SiteInfo.objects.filter(user_id=request.session['user_id'], is_default=True)
    site = sites[0]
    # 获取地址详细信息
    sperson = site.sperson
    sphone = site.sphone
    saddress = site.saddress
    spostcode = site.spostcode
    # 构建Json数据
    context = {'sperson': sperson, 'sphone': sphone, 'saddress': saddress, 'spostcode': spostcode, 'font_flag': 'user_center'}
    return render(request, 'df_user/user_center_site.html', context)
