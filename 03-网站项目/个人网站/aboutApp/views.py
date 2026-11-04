from django.shortcuts import render


ACHIEVEMENTS = [
    {
        'title': '华为 ICT 网络赛道省级三等奖',
        'desc': '围绕网络规划、设备配置和故障排查能力完成竞赛训练与实践。',
    },
    {
        'title': '校级“8+6”工程实践优秀个人作品三等奖',
        'desc': '在校级工程实践中完成作品设计、实现和展示，强化项目推进能力。',
    },
    {
        'title': '大学生“三下乡”社会实践',
        'desc': '负责采访、线索搜集和人员对接，提升现场沟通与信息采集能力。',
    },
]


def survey(request):
    return render(request, 'survey.html', {
        'active_menu': 'about',
        'sub_menu': 'survey',
    })


def honor(request):
    return render(request, 'honor.html', {
        'active_menu': 'about',
        'sub_menu': 'honor',
        'achievements': ACHIEVEMENTS,
    })
