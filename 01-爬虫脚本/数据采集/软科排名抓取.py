"""
有需要本节课的源码和Python软件的同学,可以一键三连后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""
import pandas as pd
from lxml import etree
from selenium import webdriver


# 启动谷歌浏览器
driver = webdriver.Chrome()

# 定义url
url = "https://www.shanghairanking.cn/rankings/bcur/2023"
# 访问url
driver.get(url)
# # 浏览器最大化
driver.maximize_window()
# 隐式等待
driver.implicitly_wait(5)

# 先创建一个数组，保存结果
contents = []

# 获取全部网页信息
html = driver.page_source
root = etree.HTML(html)

# 使用 XPath 选择tbody下的所有tr节点
school_info_list = root.xpath('//tbody/tr')


for school_info in school_info_list:
    contents.append([
        school_info.xpath('./td[1]/div/text()')[0].replace('\n', '').replace(' ', ''),
        school_info.xpath('./td[2]/div/div[2]/div[1]/div/div/a/text()')[0].replace('\n', '').replace(' ', ''),
        school_info.xpath('./td[3]/text()')[0].replace('\n', '').replace(' ', ''),
        school_info.xpath('./td[4]/text()')[0].replace('\n', '').replace(' ', ''),
        school_info.xpath('./td[5]/text()')[0].replace('\n', '').replace(' ', ''),
        school_info.xpath('./td[6]/text()')[0].replace('\n', '').replace(' ', ''),
    ])

print(contents)

first_name = ["排名", "学校名称", "省市", "类型", "总分", "办学层次"]
rank = pd.DataFrame(contents, columns=first_name)
# 将字符串转为int或float类型
rank["排名"] = rank["排名"].astype(int)
rank["总分"] = rank["总分"].astype(float)
# pd.to_numeric函数errors参数设为'coerce'，可以将无效解析设置为NaN
rank["办学层次"] = rank["办学层次"].apply(pd.to_numeric, errors='coerce')
print(rank.head())

rank.to_excel("2023中国大学排名.xlsx", index=False)
print("保存成功！")


"""
有需要本节课的源码和Python软件的同学,可以一键三连后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""