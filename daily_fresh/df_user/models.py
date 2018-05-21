from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ushou = models.CharField(max_length=20, default='', null=True)
    uaddress = models.CharField(max_length=100, default='', null=True)
    uyoubian = models.CharField(max_length=6, default='', null=True)
    uphone = models.CharField(max_length=11, default='', null=True)

    # default blank是python层面的约束，不影响数据库结构
    # null是数据库层面的约束，会影响数据库结构

    class Meta:
        ordering = ['pk', 'uname']

