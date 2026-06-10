from django.urls import path
from . import views

app_name = 'productsApp'
urlpatterns = [
    path('products/network/', views.products, {'productName': 'network'}, name='network'),
    path('products/python/', views.products, {'productName': 'python'}, name='python'),
    path('products/tool/', views.products, {'productName': 'tool'}, name='tool'),
    path('products/robot/', views.products, {'productName': 'robot'}, name='robot'),
    path('products/monitor/', views.products, {'productName': 'monitor'}, name='monitor'),
    path('products/monitoring/', views.products, {'productName': 'monitor'}, name='monitoring'),
    path('products/face/', views.products, {'productName': 'face'}, name='face'),
    path('productDetail/<int:id>/', views.productDetail, name='productDetail'),
    path('products/<str:productName>/', views.products, name='products'),
]
