# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-21 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0005_auto_20180521_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='siteinfo',
            options={'ordering': ['pk', 'user']},
        ),
        migrations.RenameField(
            model_name='siteinfo',
            old_name='syoubian',
            new_name='spostcode',
        ),
    ]
