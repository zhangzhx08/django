from django.db import models

class OrderInfo(models.Model):
    odate = models.DateField(auto_now=True)
    user = models.ForeignKey('df_user.UserInfo')
    ototle = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150)
    is_pay = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.user.uname+':'+str(self.id)


class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')
    ocount = models.IntegerField()
    order = models.ForeignKey(OrderInfo)

    class Meta:
        ordering = ['order_id']

    def __str__(self):
        return self.goods.gtitle + '-' + str(self.ocount) + ':' + self.order_id
