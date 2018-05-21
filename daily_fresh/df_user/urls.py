# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_haddle/$', views.login_handle, name='login_haddle'),
    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^user_center_order/$', views.user_center_order, name='user_center_order'),
    url(r'^user_center_site/$', views.user_center_site, name='user_center_site'),

]
