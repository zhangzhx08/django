# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-22 12:41
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20180522_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsinfo',
            name='gdetail',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]
