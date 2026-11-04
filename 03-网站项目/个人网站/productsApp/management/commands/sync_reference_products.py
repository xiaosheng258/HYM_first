import os
import re
from decimal import Decimal, InvalidOperation
from html import unescape
from datetime import timedelta
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from django.conf import settings
from django.db import connection
from django.core.management.base import BaseCommand
from django.utils import timezone

from productsApp.models import Product, ProductImage


BASE_URL = 'http://47.103.207.39/'
CATEGORIES = {
    'robot': '家用机器人',
    'monitor': '智能监控',
    'face': '人脸识别解决方案',
}


class Command(BaseCommand):
    help = 'Sync product center data and images from the reference website.'

    def handle(self, *args, **options):
        product_dir = os.path.join(settings.MEDIA_ROOT, 'Product')
        os.makedirs(product_dir, exist_ok=True)

        synced = 0
        synced_source_ids = set()
        for product_type in CATEGORIES:
            items = list(self.fetch_category(product_type))
            base_time = timezone.now()
            for index, item in enumerate(items):
                detail = self.fetch_detail(item['detail_url'])
                item.update(detail)
                if not item['image_urls']:
                    item['image_urls'] = item['list_image_urls']
                item['publishDate'] = base_time - timedelta(minutes=index)
                image_paths = []
                for image_url in item['image_urls']:
                    image_name = self.download_image(image_url, product_dir)
                    if image_name:
                        image_paths.append('Product/%s' % image_name)
                product = self.upsert_product(product_type, item, image_paths)
                if product.sourceId:
                    synced_source_ids.add(product.sourceId)
                synced += 1
                self.stdout.write('%s %s' % (product_type, product.title))

        if synced_source_ids:
            stale_products = Product.objects.exclude(sourceId__in=synced_source_ids)
            stale_ids = list(stale_products.values_list('id', flat=True))
            ProductImage.objects.filter(product__in=stale_products).delete()
            self.delete_legacy_product_images(stale_ids)
            stale_products.delete()

        self.stdout.write(self.style.SUCCESS('Synced %s products.' % synced))

    def delete_legacy_product_images(self, product_ids):
        if not product_ids:
            return
        table_names = connection.introspection.table_names()
        if 'productsApp_productimg' not in table_names:
            return
        placeholders = ','.join(['%s'] * len(product_ids))
        with connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM productsApp_productimg WHERE product_id IN (%s)' % placeholders,
                product_ids,
            )

    def fetch_url(self, url):
        with urlopen(url, timeout=20) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.read().decode(charset, errors='ignore')

    def fetch_category(self, product_type):
        first_url = urljoin(BASE_URL, 'productsApp/products/%s/' % product_type)
        first_html = self.fetch_url(first_url)
        max_page = self.get_max_page(first_html)
        seen = set()

        for page in range(1, max_page + 1):
            url = first_url if page == 1 else first_url + '?page=%s' % page
            html = first_html if page == 1 else self.fetch_url(url)
            pattern = (
                r'<a href="(?P<detail>[^"]*productDetail/\d+/)" class="thumbnail row-4">\s*'
                r'<img[^>]+src="(?P<image>[^"]+)"[^>]*>\s*</a>.*?'
                r'<h3>(?P<title>.*?)</h3>\s*'
                r'<p>(?P<summary>.*?)</p>'
            )
            for match in re.finditer(pattern, html, re.S):
                detail_url = urljoin(BASE_URL, match.group('detail'))
                if detail_url in seen:
                    continue
                seen.add(detail_url)
                source_match = re.search(r'productDetail/(\d+)/', detail_url)

                yield {
                    'sourceId': int(source_match.group(1)) if source_match else None,
                    'detail_url': detail_url,
                    'list_image_urls': [urljoin(BASE_URL, match.group('image'))],
                    'title': self.clean_text(match.group('title')),
                    'description': self.clean_text(match.group('summary')),
                }

    def fetch_detail(self, detail_url):
        html = self.fetch_url(detail_url)
        description = ''
        price = None

        intro = re.search(r'<h3>\s*产品介绍\s*</h3>\s*<p>\s*(.*?)\s*</p>\s*<h3>', html, re.S)
        if intro:
            description = intro.group(1).strip()

        price_match = re.search(r'<h3>\s*参考价格\s*</h3>\s*<p>\s*([^<]+)\s*</p>', html, re.S)
        if price_match:
            price = self.parse_price(price_match.group(1))

        return {
            'description': description,
            'price': price,
            'image_urls': self.fetch_detail_images(html),
        }

    def fetch_detail_images(self, html):
        images = []
        for image in re.findall(r'<div class="row-4">\s*<img[^>]+src="([^"]+)"', html, re.S):
            images.append(urljoin(BASE_URL, image))
        return images

    def get_max_page(self, html):
        pages = [int(page) for page in re.findall(r'\?page=(\d+)', html)]
        return max(pages) if pages else 1

    def clean_text(self, value):
        value = re.sub(r'<br\s*/?>', '\n', value, flags=re.I)
        value = re.sub(r'</p>\s*<p>', '\n\n', value, flags=re.I)
        value = re.sub(r'<[^>]+>', '', value)
        value = unescape(value)
        value = re.sub(r'[ \t\r\f\v]+', ' ', value)
        value = re.sub(r'\n\s+', '\n', value)
        return value.strip()

    def parse_price(self, value):
        match = re.search(r'[\d.]+', value)
        if not match:
            return None
        try:
            return Decimal(match.group(0))
        except InvalidOperation:
            return None

    def download_image(self, image_url, product_dir):
        if not image_url:
            return ''
        parsed = urlparse(image_url)
        image_name = os.path.basename(parsed.path)
        if not image_name:
            return ''

        target = os.path.join(product_dir, image_name)
        if not os.path.exists(target):
            with urlopen(image_url, timeout=20) as response:
                content = response.read()
            with open(target, 'wb') as image_file:
                image_file.write(content)
        return image_name

    def upsert_product(self, product_type, item, image_paths):
        product, _ = Product.objects.update_or_create(
            title=item['title'],
            defaults={
                'sourceId': item['sourceId'],
                'description': item['description'],
                'productType': product_type,
                'price': item['price'],
                'publishDate': item['publishDate'],
                'views': 0,
            },
        )

        if image_paths:
            product.images.all().delete()

        seen_paths = set()
        for index, image_path in enumerate(image_paths):
            if image_path in seen_paths:
                continue
            seen_paths.add(image_path)
            ProductImage.objects.create(
                product=product,
                description='%s-%s' % (item['title'], index + 1),
                photo=image_path,
            )

        return product
