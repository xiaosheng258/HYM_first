from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sourceId', 'title', 'productType', 'price', 'publishDate', 'views')
    list_filter = ('productType',)
    search_fields = ('title', 'description')
    fields = ('sourceId', 'title', 'description', 'productType', 'price', 'publishDate', 'views')
    inlines = (ProductImageInline,)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'description', 'created')
    list_filter = ('product__productType',)
    search_fields = ('product__title', 'description')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
