# Generated to record the legacy products table that already exists in db.sqlite3.

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='产品标题')),
                ('description', models.TextField(verbose_name='产品详情描述')),
                ('productType', models.CharField(choices=[('robot', '家用机器人'), ('monitor', '智能监控'), ('face', '人脸识别解决方案')], max_length=50, verbose_name='产品类型')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='产品价格')),
                ('publishDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品',
                'ordering': ('-publishDate',),
            },
        ),
    ]
