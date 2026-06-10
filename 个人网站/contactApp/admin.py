from django.contrib import admin
from django.http import FileResponse

from .models import ContactInfo, JobPosition, Resume
from .utils import build_resume_docx


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('company', 'phone', 'fax', 'website')


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'ordering', 'is_active', 'created')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('ordering', 'is_active')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'edu', 'position', 'email', 'created')
    list_filter = ('sex', 'edu', 'position', 'created')
    search_fields = ('name', 'personID', 'email', 'school', 'major', 'position')
    readonly_fields = ('created',)
    actions = ('export_word',)

    def export_word(self, request, queryset):
        output = build_resume_docx(queryset)
        return FileResponse(
            output,
            as_attachment=True,
            filename='resume.docx' if queryset.count() == 1 else 'resumes.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )

    export_word.short_description = '导出所选简历为Word文档'
