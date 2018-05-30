from django.db import models
# from df_user.models import *
# from df_goods.models import *


class CartInfo(models.Model):
    # 同一项目中不同app之间，models的外键可以通过导入其它应用的models，
    # 也可以直接以'app_name.ClassName'的方式调用
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField(default=1)
    is_selected = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk', 'goods']
