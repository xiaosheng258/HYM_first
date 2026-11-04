from django.contrib import admin

from .models import Award


class AwardAdmin(admin.ModelAdmin):
    list_display = ['description', 'photo']


admin.site.register(Award, AwardAdmin)
admin.site.site_header = '胡一鸣个人网站后台'
admin.site.site_title = '胡一鸣个人网站后台'
