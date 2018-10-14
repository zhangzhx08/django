# -*- coding:utf-8 -*-

import os
from celery import Celery
from df_celery.tasks import periodic_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_fresh.settings')

app = Celery('daily_fresh')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.add_periodic_task(5, periodic_task)
