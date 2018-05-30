from django.contrib import admin
from .models import *


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'odate', 'user', 'ototle', 'oaddress', 'is_pay']
    list_filter = ['user']
    list_per_page = 20
    search_fields = ['id', 'user']


class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'goods', 'ocount', 'order']
    list_filter = ['goods', 'order']
    list_per_page = 20
    search_fields = ['goods', 'order']


admin.site.register(OrderInfo,OrderInfoAdmin)
admin.site.register(OrderDetailInfo, OrderDetailInfoAdmin)
