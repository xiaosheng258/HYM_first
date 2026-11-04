"""URL configuration for Hu Yiming's personal site."""
from django.contrib import admin
from django.urls import path, include
from homeApp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('aboutApp/', include('aboutApp.urls')),
    path('newsApp/', include('newsApp.urls')),
    path('productsApp/', include('productsApp.urls')),
    path('tools/', include('toolsApp.urls')),
    path('scienceApp/', include('scienceApp.urls')),
    path('contactApp/', include('contactApp.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('search/', include('haystack.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
