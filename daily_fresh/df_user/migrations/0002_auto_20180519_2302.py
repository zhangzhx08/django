# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-19 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'ordering': ['uname', 'uaddress']},
        ),
    ]