from django.db import models
# from df_user.models import *
# from df_goods.models import *


class CartInfo(models.Model):
    count = models.IntegerField(default=1)
    # 同一项目中不同app之间，models的外键可以通过导入其它应用的models，
    # 也可以直接以'app_name.ClassName'的方式调用
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')

    class Meta:
        ordering = ['pk', 'goods']
