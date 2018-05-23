from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ctitle', 'cpic', 'cclass', 'is_delete']
    list_filter = ['ctitle']
    list_per_page = 10
    search_fields = ['ctitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'gtitle', 'gpic', 'gprice',
                    'gunit', 'gintro', 'gsales', 'ginventory',
                    'gclick', 'is_delete', 'category'
                    ]
    list_filter = ['gtitle', 'category']
    list_per_page = 10
    search_fields = ['gtitle', 'category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
