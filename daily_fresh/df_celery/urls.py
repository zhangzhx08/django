# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'celery_test/', views.celery_test, name='celery_test')
]