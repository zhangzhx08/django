# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-20 07:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180519_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='uemain',
            new_name='uemail',
        ),
    ]
