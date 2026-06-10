from django.urls import path

from . import views

app_name = 'toolsApp'

urlpatterns = [
    path('', views.bilidown, name='index'),
    path('bilidown/', views.bilidown, name='bilidown'),
    path('download/', views.bilidown, name='download'),
    path('platform/', views.bilidown, name='platform'),
]

