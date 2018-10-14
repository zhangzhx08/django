# -*- coding:utf-8 -*-

from celery import shared_task
import time


@shared_task
def periodic_task():
    print('这是celery任务正在执行!')
    time.sleep(5)
    print('celery任务执行完毕!')
    return
