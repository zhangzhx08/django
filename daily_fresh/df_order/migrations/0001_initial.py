# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-27 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('df_goods', '0005_category_cpic'),
        ('df_user', '0009_auto_20180521_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocount', models.IntegerField()),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_goods.GoodsInfo')),
            ],
            options={
                'ordering': ['order_id'],
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('odate', models.DateField(auto_now=True)),
                ('ototle', models.DecimalField(decimal_places=2, max_digits=6)),
                ('oaddress', models.CharField(max_length=150)),
                ('ois_pay', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_user.UserInfo')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_order.OrderInfo'),
        ),
    ]