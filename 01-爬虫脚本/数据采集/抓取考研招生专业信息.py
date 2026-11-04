"""
有需要本节课的源码和Python软件的同学,可以一键三连后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""
import requests
import pandas as pd
from lxml import etree  # 导入xpath解析数据


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"
}


url = "https://yz.chsi.com.cn/zsml/queryAction.do"

params = {
    "ssdm": "43",               # 省份代码
    "dwmc": "",                 # 学校名称
    "mldm": "08",               # 学术学位 或 专业学位 的拼音缩写
    "mlmc": "",
    "yjxkdm": "0812",           # 专业领域代码
    "zymc": "计算机科学与技术",    # 学科名称
    "xxfs": 1,      # 预设全日制本科，1 全日制， 2 非全日制
    "pageno": 1     # 预设页数为1
}

# 储存数据的列表
table = []


def getSearchData():
    return requests.get(url, headers=headers, params=params).content.decode("utf-8")


def getARecored(data, schoolInfo):
    data_xpath = etree.HTML(requests.get("https://yz.chsi.com.cn" + data, headers=headers, params=params).content.decode("utf-8"))
    # 将解析出来的数据打包成字典
    school_data = {
        "学校": data_xpath.xpath("//table[@class='zsml-condition']/tbody/tr[1]/td[@class='zsml-summary'][1]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "研究生院": schoolInfo["gso"],
        "自主划线": schoolInfo["ao"],
        "博士点": schoolInfo["phd"],
        "考试方式": data_xpath.xpath("//table[@class='zsml-condition']/tbody/tr[1]/td[@class='zsml-summary'][2]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "院系所": data_xpath.xpath("//table[@class='zsml-condition']/tbody/tr[2]/td[@class='zsml-summary'][1]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "专业": data_xpath.xpath("//table[@class='zsml-condition']/tbody/tr[2]/td[@class='zsml-summary'][2]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "研究方向": data_xpath.xpath("//table[@class='zsml-condition']/tbody/tr[3]/td[@class='zsml-summary'][2]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "拟招人数": data_xpath.xpath("//table[@class='zsml-condition']/tbody/tr[4]/td[@class='zsml-summary'][2]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "政治": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[1]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "政治详情": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[1]/span[@class='sub-msg']/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "英语": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[2]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "英语详情": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[2]/span[@class='sub-msg']/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "业务课一": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[3]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "业务课一详情": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[3]/span[@class='sub-msg']/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "业务课二": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[4]/text()")[0].replace('\r', '').replace('\n', '').replace(' ', ''),
        "业务课二详情": data_xpath.xpath("//table/tbody[@class='zsml-res-items'][1]/tr/td[4]/span[@class='sub-msg']/text()")[0].replace('\r', '').replace('\n', '').replace(' ', '')
    }
    print("学校信息：", school_data)
    # 将获取的字典数据追加到页面中
    table.append(school_data)


def getASchoolData(data, schoolInfo):
    data_xpath = etree.HTML(requests.get("https://yz.chsi.com.cn" + data, headers=headers, params=params).content.decode("utf-8"))
    result = data_xpath.xpath("//table/tbody/tr/td[8]/a/@href")  # 查看详细信息连接
    for i in result:
        getARecored(i, schoolInfo)


def getAPageData(data):
    data_xpath = etree.HTML(data)
    school_names = data_xpath.xpath('//*[@id="form3"]/a/text()')  # 学校名
    mid_urls = data_xpath.xpath('//*[@id="form3"]/a/@href')  # 中间网址，进一步访问每一个学校此专业的搜索结果
    graduate_school_opt = data_xpath.xpath('//table[@class="ch-table"]/tbody/tr/td[1]')  # 是否研究生院
    autonomous_opt = data_xpath.xpath('//table[@class="ch-table"]/tbody/tr/td[2]')  # 是否是自主划线院校
    PhD_point_opt = data_xpath.xpath('//table[@class="ch-table"]/tbody/tr/td[3]')  # 是否是博士点
    return [school_names, mid_urls, graduate_school_opt, autonomous_opt, PhD_point_opt]


def anlysisLoop(data):
    data_xpath = etree.HTML(data)
    max_page_num = data_xpath.xpath("/html/body//div[4]/ul/li/a/text()")[-1]  # 最大页数
    for k in range(1, int(max_page_num) + 1):
        params["pageno"] = k
        apage = getAPageData(requests.get(url, headers=headers, params=params).content.decode("utf-8"))
        for s in range(len(apage[1])):
            schoolInfo = {}
            for i in range(2, 5):
                if len(apage[i][s].xpath("./i")) != 0:
                    schoolInfo[["gso", "ao", "phd"][i - 2]] = 1
                else:
                    schoolInfo[["gso", "ao", "phd"][i - 2]] = 0
            getASchoolData(apage[1][s], schoolInfo)


data = getSearchData()
anlysisLoop(data)
df = pd.DataFrame(table)
df.to_csv("考研招生.csv", index=False)
# 存储到 csv 文件


"""
有需要本节课的源码和Python软件的同学,可以一键三连后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""