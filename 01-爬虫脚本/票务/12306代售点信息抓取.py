"""
有需要本节课的源码和Python软件的同学,可以一键三连后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""
import time
import requests
import pandas as pd
from datetime import datetime

url = "https://kyfw.12306.cn/otn/userCommon/allProvince"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

content_json = requests.get(url=url, headers=headers).json()
print("等待3s")
time.sleep(3)  # 防止被检测（不要低于3）
print(content_json)  # 用于观察
# df = pd.DataFrame(content_json['data'])
content_list = pd.json_normalize(content_json['data'], errors='ignore')

if __name__ == '__main__':
    # 当前时间作为文件名后缀
    curr_time = datetime.now()
    timestamp = datetime.strftime(curr_time, '%Y-%m-%d %H-%M-%S')
    # time = time.time()  # 时间

    # 将 DataFrame 保存为 excel 文件
    content_list.to_excel(f"全国火车票代售点的省-{timestamp}.xlsx", index=False)
    print("保存完成！")

    # 查看 DataFrame 的行数和列数。
    rows = content_list.shape
    print("请求得到的表格行数与列数：", rows)

"""
有需要本节课的源码和Python软件的同学,可以一键三连后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""