# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from .models import *
from django.http import request, HttpResponse, JsonResponse, response
from django.core.urlresolvers import reverse
from hashlib import sha1


# 用户注册
def register(request):
    cookie = request.COOKIES
    # context = {}
    # if 'uname' in cookie:
    uname = cookie.get('uname', '')
    uemail = cookie.get('uemail', '')
    context = {'uname': uname, 'uemail': uemail}
    return render(request, 'df_user/register.html', context)


# 判断用户名是否存在
def register_exist(request):
    uname = request.GET.get('user_name')
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
        uname = post.get('user_name')
        uemail = post.get('email')
        # context = {'uname': uname, 'uemail': uemail}
        # res = render(request, 'df_user/register.html', context)
        res = render(request, 'df_user/register.html')
        res.set_cookie('uname', uname, max_age=300)
        res.set_cookie('uemail', uemail, max_age=300)
        return res


# 登录
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'uname': uname, 'error_name': False, 'error_pwd': False}
    return render(request, 'df_user/login.html', context)


# 登录处理
def login_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    remember = post.get('remember', '0')
    users = UserInfo.objects.filter(uname=uname)
    # 判断用户名是否存在
    if len(users) == 1:
        # 密码加密处理
        s = sha1()
        s.update(upwd.encode())
        upwd_sha = s.hexdigest()
        # 判断密码是否正确
        if upwd_sha == users[0].upwd:
            res = redirect(reverse('df_user:user_center_info'))
            # 设置cookie，记住用户名
            if remember != '0':
                res.set_cookie('uname', uname)
            else:
                res.set_cookie('uname', '', max_age=-1)
            # 设置session，状态保持
            request.session['user_id'] = users[0].id
            request.session['uname'] = uname
            request.session.set_expiry(3600)
            return res
        else:
            context = {'uname': uname, 'error_name': False, 'error_pwd': True}
            return render(request, 'df_user/login.html', context)
    else:
        # context = {'uname': uname, 'error_name': True, 'error_pwd': False}
        # return render(request, 'df_user/login.html', context)
        redi = redirect(reverse('df_user:login'))
        redi.set_cookie('uname', uname)
        redi.set_cookie('error_nama', False)
        redi.set_cookie('error_pwd', False)
        context = {'uname': uname, 'error_name': False, 'error_pwd': False}
        
        return redi


# 用户中心信息
def user_center_info(request):
    return render(request, 'df_user/user_center_info.html')


def user_center_order(request):
    return render(request, 'df_user/user_center_order.html')


def user_center_site(request):
    return render(request, 'df_user/user_center_site.html')
