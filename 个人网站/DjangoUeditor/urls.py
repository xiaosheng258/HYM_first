# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import get_ueditor_controller

urlpatterns = [
    re_path(r'^controller/$', get_ueditor_controller),
]