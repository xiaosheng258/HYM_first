"""
有需要本节课的源码和Python软件的同学,可以一键三连,在评论区留言,我会发给你的,也可以直接私信我领取！
"""
import re
import json
import requests
import pandas as pd

# 定义一个空的列表，存放每一页的数据
df_list = []

# for循环用来获取不同页码的数据，这里循环10次
for index in range(1, 10):
    # 请求的url地址或者接口,页面数使用花括号占位
    url = f"http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18306600264369919882_1675428357095&fundCode=519185&pageIndex={index}&pageSize=20&startDate=&endDate=&_=1705304941986"

    # 请求所需要的请求头内容
    headers = {
        "Host": "api.fund.eastmoney.com",
        # 防盗链   确定访问来路是否非法
        "Referer": "http://fundf10.eastmoney.com/",
        # 身份验证，模拟浏览器发出
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
    }

    # 发送请求
    resp = requests.get(url, headers=headers)

    # 打印获取的数据
    data = resp.text
    print(data)

    # 通过正则表达式获取只想要的数据
    data = re.findall("\((.*?)\)", data)
    # print(data)

    # 将数据转换成json格式
    data = json.loads(data[0])["Data"]["LSJZList"]
    print(data)

    # 使用pandas格式化数据
    df = pd.DataFrame(data)
    print(df)

    # 将每一页数据添加到列表中
    df_list.append(df)

# 打印列表中的所有数据
# print(df_list)

# 合并列表中的数据
df_data = pd.concat(df_list)
# print(df_data)

# 将数据保存到csv中,行号不保存
df_data.to_csv("万家精选混合A (519185).csv", index=False)


"""
有需要本节课的源码和Python软件的同学,可以一键三连,在评论区留言,我会发给你的,也可以直接私信我领取！
"""