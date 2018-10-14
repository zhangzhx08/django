# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from . import tasks


def celery_test(request):
    tasks.periodic_task.delay()
    context = {'status': 'celery正在后台执行任务，页面提前返回！'}
    return JsonResponse(context)
