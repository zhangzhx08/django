# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-28 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0002_auto_20180527_2240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderinfo',
            options={'ordering': ['pk']},
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
