# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-21 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0007_siteinfo_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteinfo',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
