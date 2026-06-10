import hashlib
import os
import re
import subprocess
import time
from urllib.parse import urlencode

import requests
from django.conf import settings


class BiliDownError(Exception):
    pass


class BiliDownloader:
    mixin_key_enc_tab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
        27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
        37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
        22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
    ]
    quality_map = {
        127: '8K 超高清',
        126: '杜比视界',
        125: 'HDR 真彩',
        120: '4K 超清',
        116: '1080P 60帧',
        112: '1080P+ 高码率',
        80: '1080P 高清',
        74: '720P 60帧',
        64: '720P 高清',
        32: '480P 清晰',
        16: '360P 流畅',
        6: '240P 极速',
    }
    quality_priority = [127, 126, 125, 120, 116, 112, 80, 74, 64, 32, 16, 6]

    def __init__(self, cookie=''):
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/119.0.0.0 Safari/537.36'
            ),
            'Referer': 'https://www.bilibili.com/',
            'Origin': 'https://www.bilibili.com',
        }
        if cookie:
            self.headers['Cookie'] = cookie
        self.download_dir = os.path.join(settings.MEDIA_ROOT, 'bilidown')
        os.makedirs(self.download_dir, exist_ok=True)
        self.ffmpeg_path = os.path.join(settings.BASE_DIR, 'toolsApp', 'bin', 'ffmpeg.exe')
        if not os.path.exists(self.ffmpeg_path):
            self.ffmpeg_path = 'ffmpeg'

    def parse_video_info(self, value):
        bvid_match = re.search(r'(BV[0-9A-Za-z]+)', value or '')
        if not bvid_match:
            raise BiliDownError('无法识别 BV 号，请输入完整 Bilibili 视频链接或 BV 号。')

        bvid = bvid_match.group(1)
        response = requests.get(
            'https://api.bilibili.com/x/web-interface/view',
            params={'bvid': bvid},
            headers=self.headers,
            timeout=(10, 20),
        )
        data = _json_data(response, 'Bilibili 视频信息解析')
        if data.get('code') != 0:
            raise BiliDownError(data.get('message') or 'Bilibili 视频信息解析失败。')

        info = data.get('data') or {}
        pages = info.get('pages') or []
        first_page = pages[0] if pages else {}
        return {
            'bvid': bvid,
            'aid': info.get('aid'),
            'cid': first_page.get('cid') or info.get('cid'),
            'title': info.get('title') or bvid,
            'owner': (info.get('owner') or {}).get('name', ''),
            'duration': info.get('duration') or 0,
            'pages': pages,
            'url': 'https://www.bilibili.com/video/%s' % bvid,
        }

    def get_video_streams(self, video_info, preferred_quality=None):
        mix_key = self._get_wbi_mix_key()
        params = {
            'bvid': video_info['bvid'],
            'aid': video_info['aid'],
            'cid': video_info['cid'],
            'qn': preferred_quality or 127,
            'fnval': 4048,
            'fnver': 0,
            'fourk': 1,
            'high_quality': 1,
        }
        params = self._generate_wbi_sign(params, mix_key)
        response = requests.get(
            'https://api.bilibili.com/x/player/wbi/playurl',
            params=params,
            headers=self.headers,
            timeout=(10, 20),
        )
        data = _json_data(response, 'Bilibili 播放地址获取')
        if data.get('code') != 0:
            raise BiliDownError(data.get('message') or 'Bilibili 播放地址获取失败。')

        play_data = data.get('data') or {}
        dash = play_data.get('dash')
        if dash:
            video = self._select_best_video_stream(dash.get('video') or [], preferred_quality)
            audio = self._select_best_audio_stream(dash.get('audio') or [])
            if not video or not audio:
                raise BiliDownError('没有找到可用的视频流或音频流。')
            return {
                'format': 'dash',
                'video_urls': self._stream_urls(video),
                'audio_urls': self._stream_urls(audio),
                'quality_desc': self.quality_map.get(int(video.get('id') or 0), '自动清晰度'),
            }

        durl = play_data.get('durl') or []
        if durl:
            selected = max(durl, key=lambda item: int(item.get('size') or 0))
            return {
                'format': 'durl',
                'video_urls': self._stream_urls(selected),
                'quality_desc': self.quality_map.get(int(play_data.get('quality') or 0), '自动清晰度'),
            }

        raise BiliDownError('没有找到可用的视频下载地址。')

    def download(self, value, preferred_quality=None):
        video_info = self.parse_video_info(value)
        stream_info = self.get_video_streams(video_info, preferred_quality)
        safe_title = self._safe_filename(video_info['title'])
        output_path = self._unique_path(os.path.join(self.download_dir, safe_title + '.mp4'))
        base_name = os.path.splitext(os.path.basename(output_path))[0]

        if stream_info['format'] == 'dash':
            video_path = self._download_file(stream_info['video_urls'], base_name + '_video.m4s')
            audio_path = self._download_file(stream_info['audio_urls'], base_name + '_audio.m4s')
            self._merge_video_audio(video_path, audio_path, output_path)
        else:
            output_path = self._download_file(stream_info['video_urls'], os.path.basename(output_path))

        rel_path = os.path.relpath(output_path, settings.MEDIA_ROOT).replace('\\', '/')
        return {
            'title': video_info['title'],
            'quality_desc': stream_info.get('quality_desc', '自动清晰度'),
            'path': output_path,
            'url': settings.MEDIA_URL + rel_path,
            'size_mb': round(os.path.getsize(output_path) / 1024 / 1024, 2),
        }

    def _download_file(self, urls, filename):
        if not urls:
            raise BiliDownError('没有可用下载地址。')
        target_path = self._unique_path(os.path.join(self.download_dir, filename))
        part_path = target_path + '.part'
        last_error = None

        for download_url in urls:
            try:
                with requests.get(download_url, headers=self.headers, stream=True, timeout=(10, 30)) as response:
                    response.raise_for_status()
                    with open(part_path, 'wb') as output:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                output.write(chunk)
                os.replace(part_path, target_path)
                return target_path
            except Exception as exc:
                last_error = exc
                if os.path.exists(part_path):
                    os.remove(part_path)
                time.sleep(1)

        raise BiliDownError('下载失败：%s' % last_error)

    def _merge_video_audio(self, video_path, audio_path, output_path):
        command = [
            self.ffmpeg_path,
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-y',
            output_path,
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as exc:
            raise BiliDownError('FFmpeg 合并失败：%s' % exc)
        finally:
            for temp_path in (video_path, audio_path):
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

    def _get_wbi_mix_key(self):
        try:
            response = requests.get(
                'https://api.bilibili.com/x/web-interface/nav',
                headers=self.headers,
                timeout=(10, 20),
            )
            data = response.json()
            wbi_img = (data.get('data') or {}).get('wbi_img') or {}
            img_key = (wbi_img.get('img_url') or '').split('/')[-1].split('.')[0]
            sub_key = (wbi_img.get('sub_url') or '').split('/')[-1].split('.')[0]
            raw_key = img_key + sub_key
            mix_key = ''.join(raw_key[i] for i in self.mixin_key_enc_tab if i < len(raw_key))[:32]
            return mix_key or None
        except Exception:
            return None

    def _generate_wbi_sign(self, params, mix_key):
        if not mix_key:
            return params
        params = {
            key: str(value).translate(str.maketrans('', '', "!'()*"))
            for key, value in params.items()
        }
        params['wts'] = int(time.time())
        sorted_params = dict(sorted(params.items()))
        query = urlencode(sorted_params)
        sorted_params['w_rid'] = hashlib.md5(('%s%s' % (query, mix_key)).encode()).hexdigest()
        return sorted_params

    def _select_best_video_stream(self, streams, preferred_quality=None):
        available = {int(stream.get('id')) for stream in streams if stream.get('id') is not None}
        if not available:
            return None
        candidates = self._candidate_qualities(preferred_quality)
        quality = next((item for item in candidates if item in available), max(available))
        same_quality = [stream for stream in streams if int(stream.get('id') or 0) == quality]
        return max(same_quality, key=lambda stream: (
            int(stream.get('bandwidth') or 0),
            int(stream.get('width') or 0) * int(stream.get('height') or 0),
        ))

    def _select_best_audio_stream(self, streams):
        if not streams:
            return None
        return max(streams, key=lambda stream: int(stream.get('bandwidth') or 0))

    def _candidate_qualities(self, preferred_quality=None):
        if preferred_quality not in self.quality_priority:
            return self.quality_priority
        return self.quality_priority[self.quality_priority.index(preferred_quality):]

    def _stream_urls(self, stream):
        urls = []
        base_url = stream.get('baseUrl') or stream.get('base_url') or stream.get('url')
        if base_url:
            urls.append(base_url)
        for key in ('backupUrl', 'backup_url'):
            values = stream.get(key) or []
            if isinstance(values, str):
                values = [values]
            urls.extend([value for value in values if value])
        return list(dict.fromkeys(urls))

    def _safe_filename(self, value):
        value = re.sub(r'[\\/:*?"<>|]+', '_', value or 'bilibili-video')
        value = re.sub(r'\s+', ' ', value).strip()
        return value[:120] or 'bilibili-video'

    def _unique_path(self, path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        index = 1
        while True:
            candidate = '%s_%s%s' % (base, index, ext)
            if not os.path.exists(candidate):
                return candidate
            index += 1


def search_videos(keyword, max_pages=1, cookie=''):
    downloader = BiliDownloader(cookie=cookie)
    videos = []
    for page in range(1, max_pages + 1):
        params = downloader._generate_wbi_sign({
            'search_type': 'video',
            'keyword': keyword,
            'page': page,
        }, downloader._get_wbi_mix_key())
        response = requests.get(
            'https://api.bilibili.com/x/web-interface/wbi/search/type',
            params=params,
            headers=downloader.headers,
            timeout=(10, 20),
        )
        data = _json_data(response, 'Bilibili 搜索')
        if data.get('code') != 0:
            raise BiliDownError(data.get('message') or 'Bilibili 搜索失败。')
        for item in (data.get('data') or {}).get('result') or []:
            bvid = item.get('bvid')
            if not bvid:
                continue
            title = (item.get('title') or '').replace('<em class="keyword">', '').replace('</em>', '')
            videos.append({
                'title': title,
                'bvid': bvid,
                'author': item.get('author') or '',
                'duration': item.get('duration') or '',
                'url': 'https://www.bilibili.com/video/%s' % bvid,
            })
    return videos


def _json_data(response, action):
    try:
        return response.json()
    except ValueError:
        raise BiliDownError(
            '%s失败：接口返回 HTTP %s，可能被 Bilibili 风控限制，请稍后重试或填写登录 Cookie。'
            % (action, response.status_code)
        )
