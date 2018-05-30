# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^place_order/$', views.place_order, name='place_order'),
    url(r'^order_haddle/$', views.order_haddle, name='order_haddle'),
]
