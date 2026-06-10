import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render


PROFILE = {
    'name': '胡一鸣',
    'phone': '19565638548',
    'email': '3346742145@qq.com',
    'school': '河北传媒学院',
    'major': '网络工程（本科）',
    'location': '河北省邢台市',
    'resume_pdf': settings.MEDIA_URL + 'resume/hu-yiming-resume.pdf',
    'resume_docx': settings.MEDIA_URL + 'resume/hu-yiming-resume.docx',
}


def contact(request):
    return render(request, 'contact.html', {
        'active_menu': 'contact',
        'sub_menu': 'contact',
        'profile': PROFILE,
    })


def recruit(request):
    return render(request, 'recruit.html', {
        'active_menu': 'contact',
        'sub_menu': 'resume',
        'profile': PROFILE,
    })


def resume_word(request, resume_id):
    path = os.path.join(settings.MEDIA_ROOT, 'resume', 'hu-yiming-resume.docx')
    if not os.path.exists(path):
        raise Http404('Resume file not found')
    return FileResponse(
        open(path, 'rb'),
        as_attachment=True,
        filename='hu-yiming-resume.docx',
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
