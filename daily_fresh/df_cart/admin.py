from django.contrib import admin

from .models import *


class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'goods', 'count', 'user', 'is_selected']
    list_filter = ['goods', 'user']
    list_per_page = 20
    search_field = ['goods', 'user']


admin.site.register(CartInfo, CartInfoAdmin)
