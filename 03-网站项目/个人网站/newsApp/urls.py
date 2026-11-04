from django.urls import path
from . import views

app_name = 'newsApp'
urlpatterns = [
    # path('company/', views.company, name='company'),
    # path('industry/', views.industry, name='industry'),
    # path('notice/', views.notice, name='notice'),
    path('news/<str:newName>/',  views.news, name='news'),
    path('newsDetail/<int:id>/', views.newsDetail, name='newsDetail'), 
    path('newDetail/<int:id>/', views.newsDetail, name='newDetail'),
    path('search/', views.search, name='search'),

    
]

 
