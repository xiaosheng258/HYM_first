from django.contrib import messages
from django.shortcuts import render

from .bilidown import BiliDownError, BiliDownloader, search_videos


QUALITY_OPTIONS = (
    ('', '自动选择最高可用清晰度'),
    ('120', '4K 超清'),
    ('116', '1080P 60帧'),
    ('112', '1080P+ 高码率'),
    ('80', '1080P 高清'),
    ('64', '720P 高清'),
    ('32', '480P 清晰'),
)


def bilidown(request):
    search_results = []
    video_info = None
    download_result = None
    form_data = {
        'keyword': '',
        'url': '',
        'cookie': '',
        'quality': '',
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        form_data.update({
            'keyword': request.POST.get('keyword', '').strip(),
            'url': request.POST.get('url', '').strip(),
            'cookie': request.POST.get('cookie', '').strip(),
            'quality': request.POST.get('quality', '').strip(),
        })

        try:
            if action == 'search':
                if not form_data['keyword']:
                    raise BiliDownError('请输入搜索关键词。')
                search_results = search_videos(form_data['keyword'], max_pages=1, cookie=form_data['cookie'])
                if not search_results:
                    messages.info(request, '没有搜索到相关视频，请换一个关键词。')
            elif action == 'parse':
                if not form_data['url']:
                    raise BiliDownError('请输入 Bilibili 视频链接或 BV 号。')
                downloader = BiliDownloader(cookie=form_data['cookie'])
                video_info = downloader.parse_video_info(form_data['url'])
                stream_info = downloader.get_video_streams(
                    video_info,
                    preferred_quality=_quality_value(form_data['quality']),
                )
                video_info['quality_desc'] = stream_info.get('quality_desc', '自动清晰度')
                messages.success(request, '视频解析成功，可以继续下载。')
            elif action == 'download':
                if not form_data['url']:
                    raise BiliDownError('请输入 Bilibili 视频链接或 BV 号。')
                downloader = BiliDownloader(cookie=form_data['cookie'])
                download_result = downloader.download(
                    form_data['url'],
                    preferred_quality=_quality_value(form_data['quality']),
                )
                messages.success(request, '下载完成，文件已保存到网站 media/bilidown 目录。')
            else:
                raise BiliDownError('未知操作。')
        except BiliDownError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, '操作失败：%s' % exc)

    return render(request, 'bilidown.html', {
        'active_menu': 'tools',
        'quality_options': QUALITY_OPTIONS,
        'search_results': search_results,
        'video_info': video_info,
        'download_result': download_result,
        'form_data': form_data,
    })


def _quality_value(value):
    if not value:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
