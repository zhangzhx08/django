from django.contrib import admin
from .models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uname', 'upwd', 'uemail', 'uphone', 'uaddress', 'ushou', 'uyoubian']
    list_filter = ['uname', 'uphone']
    list_per_page = 2
    search_fields = ['uname', 'uphone']


admin.site.register(UserInfo, UserInfoAdmin)
