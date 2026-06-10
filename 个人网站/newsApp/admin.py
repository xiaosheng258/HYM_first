from django.contrib import admin
from .models import MyNews


# Register your models here.

class MyNewsAdmin(admin.ModelAdmin):
    style_fields = {
        'description': 'ueditor',
    }
    list_display = ('title', 'newType', 'publishDate', 'views')
    list_filter = ('newType', 'publishDate')
    search_fields = ('title', 'description')
    date_hierarchy = 'publishDate'
    ordering = ('-publishDate',)

admin.site.register(MyNews, MyNewsAdmin)
