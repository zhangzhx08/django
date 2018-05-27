from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    uaddress = models.CharField(max_length=100, default='', null=True, blank=True)
    uphone = models.CharField(max_length=11, default='', null=True, blank=True)

    # default blank是python层面的约束，不影响数据库结构
    # null是数据库层面的约束，会影响数据库结构

    class Meta:
        ordering = ['pk', 'uname']

    def __str__(self):
        return self.uname

class SiteInfo(models.Model):
    '''收货地址类'''
    sperson = models.CharField(max_length=20)
    saddress = models.CharField(max_length=100)
    spostcode = models.CharField(max_length=6, default='', null=True)
    sphone = models.CharField(max_length=11)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo)

    class Meta:
        ordering = ['pk', 'user']

    def __str__(self):
        return self.sperson+'/'+self.saddress+'/'+self.sperson

