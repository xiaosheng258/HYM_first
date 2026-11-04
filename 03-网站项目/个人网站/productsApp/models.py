from django.db import models
from django.utils.html import strip_tags
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    PRODUCT_TYPE = (
        ('robot', '家用机器人'),
        ('monitor', '智能监控'),
        ('face', '人脸识别解决方案'),
    )

    sourceId = models.PositiveIntegerField(null=True, blank=True, unique=True, verbose_name='参考站编号')
    title = models.CharField(max_length=100, verbose_name='产品标题')
    description = models.TextField(blank=True, verbose_name='产品详情描述')
    photo = models.ImageField(upload_to='products/', blank=True, verbose_name='产品图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='产品价格')
    productType = models.CharField(max_length=20, choices=PRODUCT_TYPE, verbose_name='产品类型')
    publishDate = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ('-publishDate',)

    def __str__(self):
        return self.title

    def detail_id(self):
        return self.sourceId or self.id

    def cover_image_url(self):
        image = self.images.first()
        if image and image.photo:
            return image.photo.url
        if self.photo:
            return self.photo.url
        return ''

    def summary(self):
        text = strip_tags(self.description or '').strip()
        if len(text) <= 180:
            return text
        return text[:179] + '…'

    def display_price(self):
        if self.price is None:
            return ''
        return format(self.price.normalize(), 'f')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='产品')
    photo = models.ImageField(upload_to='Product/', verbose_name='产品图片')
    description = models.CharField(max_length=100, blank=True, verbose_name='图片说明')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'
        ordering = ('id',)

    def __str__(self):
        return self.description or self.product.title
