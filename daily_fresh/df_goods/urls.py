# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^list/(\d+)/(\w+)/(\d+)/$', views.list, name='list'),
    url(r'^detail/(\d+)/$', views.detail, name='detail'),
]