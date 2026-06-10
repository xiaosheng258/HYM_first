from django.db import migrations


def create_initial_data(apps, schema_editor):
    ContactInfo = apps.get_model('contactApp', 'ContactInfo')
    JobPosition = apps.get_model('contactApp', 'JobPosition')

    if not ContactInfo.objects.exists():
        ContactInfo.objects.create(
            company='恒达科技有限公司',
            english_name='HengDa Science and Technology',
            business_one='111-111111',
            business_two='222-222222',
            phone='0111-1111111',
            fax='0222-2222222',
            address='某某路某某大道某某号',
            postcode='2222-222222',
            website='http://python3web.com',
            map_lng=121.506377,
            map_lat=31.245105,
            marker_lng=121.507015,
            marker_lat=31.243978,
            map_content='python web企业门户网站开发实战',
        )

    positions = [
        (
            '项目经理',
            '岗位职责：1、负责制订项目计划和方案，并组织实施；2、负责项目需求分析、设计、开发等项目全过程管理工作；',
        ),
        (
            'UI设计师',
            'UI设计师岗位职责：1、负责软件界面的美术设计、创意工作和制作工作；2、根据各种相关软件的用户群，提出构思新颖、有高度吸引力的创意设计。岗位要求：1、精通Photoshop、Illustrator、Flash等图形软件，html、Dreamweaver等网页制作工具，能够独立完成静态网页设计工作；2、熟练操作常用办公软件，且具备其它软件应用能力。',
        ),
        (
            '视觉算法工程师',
            '岗位职责：1、根据用户检测需求，评估图像算法实现可行性；2、与机械、电气工程师做有效协作，制定视觉检测的配件安装方案、电控方案；3、参与或负责视觉配件选型、评估、测试；4、结合具体项目应用，进行图像分析、识别及理解等算法开发；5、设计开发检测软件并参与现场调试和优化。',
        ),
    ]
    for index, (title, description) in enumerate(positions, start=1):
        JobPosition.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'ordering': index,
                'is_active': True,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, migrations.RunPython.noop),
    ]
