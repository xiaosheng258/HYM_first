import requests
from lxml import etree
from openpyxl import Workbook

base_url = 'http://search.cnki.com.cn/Search/ListResult'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}


def get_page_text(url, headers, search_word, page_num):
    data = {
        'searchType': 'MulityTermsSearch',
        'ArticleType': '',
        'ReSearch': '',
        'ParamIsNullOrEmpty': 'false',
        'Islegal': 'false',
        'Content': search_word,
        'Theme': '',
        'Title': '',
        'KeyWd': '',
        'Author': '',
        'SearchFund': '',
        'Originate': '',
        'Summary': '',
        'PublishTimeBegin': '',
        'PublishTimeEnd': '',
        'MapNumber': '',
        'Name': '',
        'Issn': '',
        'Cn': '',
        'Unit': '',
        'Public': '',
        'Boss': '',
        'FirstBoss': '',
        'Catalog': '',
        'Reference': '',
        'Speciality': '',
        'Type': '',
        'Subject': '',
        'SpecialityCode': '',
        'UnitCode': '',
        'Year': '',
        'AcefuthorFilter': '',
        'BossCode': '',
        'Fund': '',
        'Level': '',
        'Elite': '',
        'Organization': '',
        'Order': '1',
        'Page': str(page_num),
        'PageIndex': '',
        'ExcludeField': '',
        'ZtCode': '',
        'Smarts': '',
    }

    response = requests.post(url=url, headers=headers, data=data)
    page_text = response.text
    return page_text


def list_to_str(my_list):
    my_str = "".join(my_list)
    return my_str


def get_abstract(url):
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    tree = etree.HTML(page_text)
    abstract = tree.xpath('//div[@class="xx_font"]//text()')
    return abstract


def parse_page_text(page_text):
    tree = etree.HTML(page_text)
    item_list = tree.xpath('//div[@class="list-item"]')
    page_info = []
    for item in item_list:
        # 标题
        title = list_to_str(item.xpath(
            './p[@class="tit clearfix"]/a[@class="left"]/@title'))
        # 链接
        link = 'https:' + \
               list_to_str(item.xpath(
                   './p[@class="tit clearfix"]/a[@class="left"]/@href'))
        # 作者
        author = list_to_str(item.xpath(
            './p[@class="source"]/span[1]/@title'))
        # 出版日期
        date = list_to_str(item.xpath(
            './p[@class="source"]/span[last()-1]/text() | ./p[@class="source"]/a[2]/span[1]/text() '))
        # 关键词
        keywords = list_to_str(item.xpath(
            './div[@class="info"]/p[@class="info_left left"]/a[1]/@data-key'))
        # 摘要
        abstract = list_to_str(get_abstract(url=link))
        # 文献来源
        paper_source = list_to_str(item.xpath(
            './p[@class="source"]/span[last()-2]/text() | ./p[@class="source"]/a[1]/span[1]/text() '))
        # 文献类型
        paper_type = list_to_str(item.xpath(
            './p[@class="source"]/span[last()]/text()'))
        # 下载量
        download = list_to_str(item.xpath(
            './div[@class="info"]/p[@class="info_right right"]/span[@class="time1"]/text()'))
        # 被引量
        refer = list_to_str(item.xpath(
            './div[@class="info"]/p[@class="info_right right"]/span[@class="time2"]/text()'))

        item_info = [i.strip() for i in
                     [title, author, paper_source, paper_type, date, abstract, keywords, download, refer, link]]
        page_info.append(item_info)
        print(page_info)
    return page_info


def write_to_excel(info, search_word):
    wb = Workbook()
    ws = wb.active  # 创建子表
    ws.title = search_word
    title = ['title', 'author', 'paper_source', 'paper_type', 'date', 'abstract', 'keywords', 'download', 'refer',
             'link']  # 设置表头
    ws.append(title)

    for row in info:
        ws.append(row)

    wb.save('data.xlsx')
    return True


# 获取页面数据
page_text = get_page_text(base_url, headers, '区块链', 1)

# 解析页面数据
page_info = parse_page_text(page_text)
# 读取excel表格

write_to_excel(page_info, '区块链')


"""
有需要这个源码和Python软件的同学可以一键三连，然后在评论区留言,我会发给大家,或者也可以直接私信我领取！
"""