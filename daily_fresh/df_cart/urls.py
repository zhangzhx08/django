# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart_add/(\d+)/(\d+)/$', views.cart_add, name='cart_add'),
    url(r'^cart_delete/(\d+)/$', views.cart_delete, name='cart_delete'),
    url(r'^cart_count/$', views.cart_count, name='cart_count'),
    url(r'^cart_edit/(\d+)/(\d+)/$', views.cart_edit, name='cart_edit'),
]