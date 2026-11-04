import requests
import os # 操作系统

# \: 转义符
filename = '恐怖听故事\\'
if not os.path.exists(filename):
    os.mkdir(filename)

# 获取数据
mulu_dizhi = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=30210574&pageNum=1&sort=0&pageSize=30'
# 反爬虫 - 请求头
headers = {
    # 浏览器的身份标识 - 伪装
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# text: 文本数据 / 源代码
# json: json
mulu_xinxi = requests.get(mulu_dizhi, headers=headers).json()

# 2. 拿取全部音频的id 以及标题
# 字典取值
mulu_xinxi = mulu_xinxi['data']['tracks']
# print(mulu_xinxi)
# for循环: 从列表中 一条条的拿取数据
for yinpin_xinxi in mulu_xinxi:
    # print(yinpin_xinxi)
    yinpin_title = yinpin_xinxi['title']
    print(yinpin_title)
    # 替换地址 拿取音频信息
    # f_string ： 字符串 变量传入
    play_dizhi = f'https://www.ximalaya.com/revision/play/v1/audio?id={yinpin_xinxi["trackId"]}&ptype=1'
    yinpin_data = requests.get(play_dizhi, headers=headers).json()
    # print(yinpin_data)
    yinpin_dizhi = yinpin_data['data']['src'] # 1    2
    print(yinpin_dizhi)

    # 打开文件 / 读写形式
    # 二进制 ： 图片 音频 视频 : content
    yinpin = open(filename + yinpin_title + '.m4a', mode='wb')
    # 写入数据
    yinpin.write(requests.get(yinpin_dizhi, headers=headers).content)
    # 关闭文件
    yinpin.close()