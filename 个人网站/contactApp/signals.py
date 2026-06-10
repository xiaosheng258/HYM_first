from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Resume


@receiver(post_save, sender=Resume)
def send_resume_notice(sender, instance, created, **kwargs):
    if not created:
        return
    message = EmailMessage(
        '新的简历投递：%s' % instance.position,
        (
            '姓名：%s\n'
            '身份证号：%s\n'
            '性别：%s\n'
            '出生日期：%s\n'
            '邮箱：%s\n'
            '学历：%s\n'
            '毕业学校：%s\n'
            '专业：%s\n'
            '申请职位：%s\n'
            '学习或工作经历：%s'
        ) % (
            instance.name,
            instance.personID,
            instance.sex,
            instance.birth.strftime('%Y-%m-%d'),
            instance.email,
            instance.edu,
            instance.school,
            instance.major,
            instance.position,
            instance.experience or '',
        ),
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
        [getattr(settings, 'CONTACT_NOTICE_EMAIL', 'webmaster@localhost')],
    )
    if instance.photo:
        try:
            message.attach_file(instance.photo.path)
        except Exception:
            pass
    message.send(fail_silently=True)
