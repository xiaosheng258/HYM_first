from django.http import Http404
from django.shortcuts import redirect, render


NOTE_CATEGORIES = {
    'network': '网络基础',
    'linux': 'Linux 运维',
    'python': 'Python 学习',
}

NOTES = [
    {
        'id': 1,
        'category': 'network',
        'title': 'TCP/IP 与路由交换学习记录',
        'date': '2026-06-01',
        'summary': '整理网络工程课程中关于 IP 编址、VLAN、路由协议和 ACL 的核心知识点。',
        'content': [
            '网络排错先从物理连通、IP 地址、网关、路由表和访问控制顺序检查。',
            '在 eNSP 实验中，我会先画拓扑和地址规划，再做逐段 ping/tracert 验证，减少配置遗漏。',
        ],
    },
    {
        'id': 2,
        'category': 'linux',
        'title': 'Linux 服务器常用操作笔记',
        'date': '2026-06-02',
        'summary': '记录用户权限、服务管理、日志排查和网络状态查看等基础运维操作。',
        'content': [
            '常用命令包括 systemctl、journalctl、ss、ip、tar、find 和 grep。',
            '部署服务时重点关注端口监听、进程状态、配置文件权限和日志输出。',
        ],
    },
    {
        'id': 3,
        'category': 'python',
        'title': 'Django 个人网站改造要点',
        'date': '2026-06-07',
        'summary': '把企业门户改造成个人站时，优先处理路由、模板、静态资源和后台工具入口。',
        'content': [
            '旧项目中大量内容来自模板和 SQLite 数据库，前台改造时应先切断旧数据展示。',
            '工具类功能适合封装为独立模块，视图只负责表单输入、异常提示和结果展示。',
        ],
    },
]


def news(request, newName):
    category = newName if newName in NOTE_CATEGORIES else 'python'
    note_list = [item for item in NOTES if item['category'] == category]
    return render(request, 'newList.html', {
        'active_menu': 'notes',
        'submenu': category,
        'newName': NOTE_CATEGORIES[category],
        'newList': note_list,
        'categories': NOTE_CATEGORIES,
    })


def newsDetail(request, id):
    note = next((item for item in NOTES if item['id'] == id), None)
    if not note:
        raise Http404('Note not found')
    return render(request, 'newsDetail.html', {
        'active_menu': 'notes',
        'mynew': note,
        'newName': NOTE_CATEGORIES[note['category']],
    })


def search(request):
    keyword = request.GET.get('keyword') or request.GET.get('q') or ''
    if not keyword:
        return redirect('newsApp:news', newName='python')
    note_list = [
        item for item in NOTES
        if keyword.lower() in item['title'].lower() or keyword.lower() in item['summary'].lower()
    ]
    return render(request, 'searchList.html', {
        'active_menu': 'notes',
        'newName': '关于 "%s" 的搜索结果' % keyword,
        'newList': note_list,
        'keyword': keyword,
    })
