# -*- coding:utf-8 -*-

from django.db import models
from tinymce.models import HTMLField


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().filter(is_delete=False)


class GoodsInfoManager(models.Manager):
    def get_queryset(self):
        return super(GoodsInfoManager, self).get_queryset().filter(is_delete=False)


class Category(models.Model):
    """商品分类"""
    ctitle = models.CharField(max_length=20)
    cclass = models.CharField(max_length=20, default='')
    cpic = models.ImageField(upload_to='categorys', null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    # objects = CategoryManager()

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.ctitle


class GoodsInfo(models.Model):
    """商品信息类"""
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=6, decimal_places=2)
    gunit = models.CharField(max_length=10)
    gintro = models.CharField(max_length=100)
    gclick = models.IntegerField()
    gsales = models.IntegerField()
    ginventory = models.IntegerField()
    is_delete = models.BooleanField(default=False)

    category = models.ForeignKey(Category)
    # objects = GoodsInfoManager()

    gdetail = HTMLField(default='')
    # gdetail = models.TextField(max_length=2000)


    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.gtitle
