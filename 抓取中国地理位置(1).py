import requests  # 第三方模块 单一功能 数据请求功能
from pprint import pprint  # 内置 格式化输出
import csv  # 内置 数据持久化


with open('肯德基.csv', mode='a', encoding='utf-8', newline='') as f:
    f.write('省份, 城市, 商圈, 具体位置, 服务\n')

# 函数
# 构建数据请求的函数 解决代码冗余的问题
def get_response(data):
    """
    def 定义一个函数的关键字
    get_response 函数的名字
    :param data: 传递的参数
    :return: 函数的返回值
    """
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    headers = {
        'Referer': 'http://www.kfc.com.cn/kfccda/storelist/index.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    json_data = requests.post(url=url, headers=headers, data=data).json()
    return json_data


# 翻页逻辑的函数
def get_page(keyword):
    data = {
        'cname': '',
        'pid': '',
        'keyword': keyword,
        'pageIndex': '1',
        'pageSize': '10',
    }
    json_da = get_response(data)
    rowcount = json_da['Table'][0]['rowcount']
    print(f'{keyword} 有 {rowcount} 家店铺')
    if rowcount % 10 > 0:
        page_num = rowcount // 10 + 1
    else:
        page_num = rowcount // 10
    print(f'{keyword} 有 {page_num} 页数据')
    return page_num


# 数据解析并且保存的函数
def get_info(keyword):
    page_num = get_page(keyword)
    for page in range(1, page_num + 1):
        data = {
            'cname': '',
            'pid': '',
            'keyword': keyword,
            'pageIndex': str(page),
            'pageSize': '10',
        }
        result = get_response(data)
        list_data = result['Table1']
        for data_1 in list_data:
            # 省份
            provinceName = data_1['provinceName']
            # 城市
            cityName = data_1['cityName']
            # 商圈
            storeName = data_1['storeName']
            # 具体位置
            addressDetail = data_1['addressDetail']
            # 服务
            pro = data_1['pro']
            print(provinceName, cityName, storeName, addressDetail, pro)

            # 数据的保存
            with open('肯德基.csv', mode='a', encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f)
                # 有序的数据容器
                csv_write.writerow([provinceName, cityName, storeName, addressDetail, pro])


if __name__ == '__main__':
    cities = ['武汉', '长沙', '南昌', '天津', '大连', '北京', '石家庄', '张家界']
    for city in cities:
        get_info(city)




# with open('肯德基.csv', mode='a', encoding='utf-8', newline='') as f:
#     f.write('省份, 城市, 商圈, 具体位置, 服务\n')
#
# for page in range(1, 9):
#     # 数据包 分析数据来源
#     url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
#
#     # 请求参数
#     data = {
#         'cname': '',
#         'pid': '',
#         'keyword': '武汉',
#         'pageIndex': str(page),
#         'pageSize': '10',
#     }
#
#     # 伪装
#     headers = {
#         'Referer': 'http://www.kfc.com.cn/kfccda/storelist/index.aspx',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
#     }
#
#     # 发送请求
#     response = requests.post(url=url, headers=headers, data=data)
#     # <Response [200]>  响应体的对象
#     # 文本数据
#     # print(response.text)
#     # json数据
#     json_data = response.json()
#     # pprint(json_data)
#
#     # 数据解析 提取我们需要的数据 二次提取 剔除我们不需要的数据
#     list_data = json_data['Table1']
#     for data_1 in list_data:
#         # 省份
#         provinceName = data_1['provinceName']
#         # 城市
#         cityName = data_1['cityName']
#         # 商圈
#         storeName = data_1['storeName']
#         # 具体位置
#         addressDetail = data_1['addressDetail']
#         # 服务
#         pro = data_1['pro']
#         print(provinceName, cityName, storeName, addressDetail, pro)
#
#         # 数据的保存
#         with open('肯德基.csv', mode='a', encoding='utf-8', newline='') as f:
#             csv_write = csv.writer(f)
#             # 有序的数据容器
#             csv_write.writerow([provinceName, cityName, storeName, addressDetail, pro])
