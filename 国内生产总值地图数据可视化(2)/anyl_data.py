#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
数据获取网址：https://data.stats.gov.cn/easyquery.htm?cn=E0103
"""

# 首先导入pyecharts里面的Map地图模块，用于绘制地图图表
from pyecharts.charts import Map

# 然后导入pyecharts里的options模块
# options是用于设置图表的配置选项，
# 例如标题、坐标轴、图例、数据标签、视觉效果等。
# 通过options参数，可以自定义图表的各种属性，以满足不同的需求。
from pyecharts import options as opts


# 再导入Pandas对用到的数据做数据处理操作
import pandas as pd

# 用pandas里的read_csv()读取指定路径下的csv文件，并且指定下编码格式：gb18030
data = pd.read_csv('分省年度数据.csv', encoding='gb18030')

# 打印一下数据的前5行（默认前5行）
print(data.head())

# 设置下年份
year = '2022年'

# 选择data数据里，地区和设置年份的这2列
info = data[['地区', year]]
# 打印下选择好的这2列的前5行内容（默认）
print(info.head())

# 将DataFrame数据（info）转换为二维列表（List of Lists）的形式，
# 其中每个内部列表对应于DataFrame的一行数据
info_list = info.values.tolist()
# 打印看下数据结构
print(info_list)

# 创建一个map对象，用来生成地图
map = Map()

"""
添加了一个名为“居民消费水平”的系列数据。
其中，data_pair参数用于设置各省份的数据，
maptype参数用于指定地图类型，这里设置为“china”，表示中国地图。
zoom参数用于设置地图的缩放级别（数字范围在0-1之间，数字越大，缩放越大），这里设置为1，表示地图显示最大缩放级别（不进行缩放）。
"""
map.add(
    series_name='居民消费水平',
    data_pair=info_list,
    maptype='china',
    zoom=1,
)

"""
使用Pyecharts中的set_global_opts()方法来设置全局配置选项，
包括图表的标题、副标题和位置等信息。

title_opts参数用于设置标题的相关选项。
我们使用了opts.TitleOpts()类来设置标题的相关选项。
title参数用于设置标题的内容，这里使用了f-string格式化字符串将变量year的值插入到标题中。
subtitle参数用于设置副标题的内容，这里设置为“数据来源：国家统计局”。
pos_right参数用于设置标题的水平位置，这里设置为“center”，表示居中对齐。
pos_top参数用于设置标题的垂直位置，这里设置为“5%”，表示距离画布顶部5%的位置


VisualMapOpts()类来设置地图图例的相关选项，包括最大值、最小值和颜色等信息。

visualmap_opts参数用于设置地图图例的相关选项
。
我们使用opts.VisualMapOpts()类来设置图例的相关选项。
max_参数用于设置图例的最大值，这里设置为53617；
min_参数用于设置图例的最小值，这里设置为10990；
range_color参数用于设置图例的颜色区间，这里设置为['#1E9600', '#FFF200', '#FF0000']，
表示从低到高分别使用绿色、黄色和红色三种颜色
"""
map.set_global_opts(
    title_opts=opts.TitleOpts(
        title=f'{year}居民消费水平（元）',
        subtitle='数据来源：国家统计局',
        pos_right='center',
        pos_top='5%'
    ),
    visualmap_opts=opts.VisualMapOpts(
        max_=53617,
        min_=10990,
        range_color=['#1E9600', '#FFF200', '#FF0000']
    )
)

# 把设置好的地图渲染成一个html文件，可以用浏览器进行打开
map.render('map.html')


