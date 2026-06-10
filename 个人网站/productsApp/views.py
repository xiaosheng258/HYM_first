from django.http import Http404
from django.shortcuts import render


PROJECT_CATEGORIES = {
    'network': '网络工程实践',
    'python': 'Python Web 项目',
    'tool': '实用工具作品',
}

PROJECTS = [
    {
        'id': 1,
        'category': 'network',
        'title': '校园网络规划与 eNSP 仿真',
        'summary': '围绕 VLAN、静态路由、OSPF 和 ACL 做网络拓扑规划，完成基础连通性、网段隔离和访问控制验证。',
        'description': [
            '基于网络工程课程训练，使用 eNSP 搭建多网段实验拓扑，完成设备配置、连通性测试和故障定位。',
            '重点覆盖路由交换技术、TCP/IP 协议理解、网络设备部署和基础网络安全策略。',
        ],
        'tech': ['eNSP', 'TCP/IP', 'VLAN', 'OSPF', 'ACL'],
    },
    {
        'id': 2,
        'category': 'python',
        'title': '个人门户网站改造',
        'summary': '将 Django 企业门户改造成个人网站，包含简历展示、作品板块、技术笔记和 BiliDown 工具入口。',
        'description': [
            '保留 Django 2.2 项目结构，重写前台模板和路由命名，移除企业站内容露出。',
            '整合个人简历信息，并把 bilidown 从桌面脚本改造成可在网页触发的工具模块。',
        ],
        'tech': ['Django', 'Bootstrap', 'SQLite', 'Python'],
    },
    {
        'id': 3,
        'category': 'tool',
        'title': 'BiliDown 视频下载工具',
        'summary': '支持 Bilibili 视频搜索、BV 链接解析、清晰度选择、音视频下载与 FFmpeg 合并。',
        'description': [
            '从本地 Tkinter 下载器提取核心下载逻辑，接入 Django 页面表单。',
            '下载结果保存到 media/bilidown，可直接从开发站点下载到本地。',
        ],
        'tech': ['requests', 'Bilibili API', 'FFmpeg', 'Django'],
    },
]


def products(request, productName):
    category = productName if productName in PROJECT_CATEGORIES else 'python'
    project_list = [item for item in PROJECTS if item['category'] == category]
    return render(request, 'productList.html', {
        'active_menu': 'projects',
        'sub_menu': category,
        'productName': PROJECT_CATEGORIES[category],
        'productList': project_list,
        'categories': PROJECT_CATEGORIES,
    })


def productDetail(request, id):
    project = next((item for item in PROJECTS if item['id'] == id), None)
    if not project:
        raise Http404('Project not found')
    return render(request, 'productDetail.html', {
        'active_menu': 'projects',
        'sub_menu': project['category'],
        'product': project,
        'productName': PROJECT_CATEGORIES[project['category']],
        'categories': PROJECT_CATEGORIES,
    })
