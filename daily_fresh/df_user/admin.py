from django.contrib import admin
from .models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uname', 'upwd', 'uemail', 'uphone', 'uaddress']
    list_filter = ['uname', 'uphone']
    list_per_page = 2
    search_fields = ['uname', 'uphone']


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sperson', 'sphone', 'spostcode', 'saddress', 'is_default']
    list_filter = ['sperson', 'sphone']
    list_per_page = 10
    search_fields = ['sperson', 'sphone']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(SiteInfo, SiteInfoAdmin)
