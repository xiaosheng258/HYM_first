from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('productsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sourceId',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='参考站编号'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='产品图片'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='产品详情描述'),
        ),
        migrations.AlterField(
            model_name='product',
            name='productType',
            field=models.CharField(choices=[('robot', '家用机器人'), ('monitor', '智能监控'), ('face', '人脸识别解决方案')], max_length=20, verbose_name='产品类型'),
        ),
        migrations.AlterField(
            model_name='product',
            name='publishDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, verbose_name='产品标题'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='Product/', verbose_name='产品图片')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='图片说明')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('product', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='images', to='productsApp.Product', verbose_name='产品')),
            ],
            options={
                'verbose_name': '产品图片',
                'verbose_name_plural': '产品图片',
                'ordering': ('id',),
            },
        ),
    ]
