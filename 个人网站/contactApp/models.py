from django.db import models
from django.utils import timezone


class ContactInfo(models.Model):
    company = models.CharField(max_length=100, default='胡一鸣个人网站', verbose_name='名称')
    english_name = models.CharField(max_length=120, default='Hu Yiming Personal Site', verbose_name='英文名称')
    business_one = models.CharField(max_length=40, default='19565638548', verbose_name='联系电话')
    business_two = models.CharField(max_length=40, default='3346742145@qq.com', verbose_name='联系邮箱')
    phone = models.CharField(max_length=40, default='19565638548', verbose_name='电话')
    fax = models.CharField(max_length=40, default='-', verbose_name='备用字段')
    address = models.CharField(max_length=200, default='河北省邢台市', verbose_name='地址')
    postcode = models.CharField(max_length=20, default='-', verbose_name='邮编')
    website = models.URLField(default='http://127.0.0.1:8000', verbose_name='网站')
    map_lng = models.DecimalField(max_digits=10, decimal_places=6, default=114.504844, verbose_name='地图经度')
    map_lat = models.DecimalField(max_digits=10, decimal_places=6, default=37.070589, verbose_name='地图纬度')
    marker_lng = models.DecimalField(max_digits=10, decimal_places=6, default=114.504844, verbose_name='标注经度')
    marker_lat = models.DecimalField(max_digits=10, decimal_places=6, default=37.070589, verbose_name='标注纬度')
    map_content = models.CharField(max_length=200, default='胡一鸣个人网站', verbose_name='地图标注说明')

    class Meta:
        verbose_name = '联系信息'
        verbose_name_plural = '联系信息'

    def __str__(self):
        return self.company


class JobPosition(models.Model):
    title = models.CharField(max_length=80, verbose_name='经历标题')
    description = models.TextField(verbose_name='经历说明')
    ordering = models.PositiveIntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        ordering = ('ordering', 'id')
        verbose_name = '经历条目'
        verbose_name_plural = '经历条目'

    def __str__(self):
        return self.title


class Resume(models.Model):
    SEX_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    EDU_CHOICES = (
        ('大专', '大专'),
        ('本科', '本科'),
        ('硕士', '硕士'),
        ('博士', '博士'),
        ('其他', '其他'),
    )

    name = models.CharField(max_length=20, verbose_name='姓名')
    personID = models.CharField(max_length=30, verbose_name='身份证号')
    sex = models.CharField(max_length=5, choices=SEX_CHOICES, default='男', verbose_name='性别')
    birth = models.DateField(verbose_name='出生日期')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    edu = models.CharField(max_length=5, choices=EDU_CHOICES, default='本科', verbose_name='学历')
    school = models.CharField(max_length=40, verbose_name='毕业学校')
    major = models.CharField(max_length=40, verbose_name='专业')
    position = models.CharField(max_length=40, verbose_name='目标方向')
    photo = models.ImageField(upload_to='Resume/', verbose_name='照片')
    experience = models.TextField(blank=True, verbose_name='学习或实践经历')
    created = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '个人简历'
        verbose_name_plural = '个人简历'

    def __str__(self):
        return '%s-%s' % (self.name, self.position)
