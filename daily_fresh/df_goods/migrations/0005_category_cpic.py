# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-23 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0004_category_cclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cpic',
            field=models.ImageField(blank=True, null=True, upload_to='categorys'),
        ),
    ]