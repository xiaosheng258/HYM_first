import datetime #模块
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
import time
#全自动化Python代码操作
from selenium import webdriver
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")









秒杀时间 = "2022-09-14 21:02:00.00000000"
打开浏览器工具 = webdriver.Chrome()



打开浏览器工具.get("https://www.taobao.com")
time.sleep(3)  #查 找  网络元素 来自 链接 文本(亲,请登录)    #点击
打开浏览器工具.find_element_by_link_text("亲，请登录").click()



#-----------------------需要登录 --------------手机扫码----------
print(f"请尽快扫码登录")
time.sleep(10)
打开浏览器工具.get("https://cart.taobao.com/cart.htm")
#----------------进入购物车-----------------------------
time.sleep(3)
# 是否全选购物车
while True:
    try:            #查找 元素 来自  ID
        if 打开浏览器工具.find_element_by_id("J_SelectAll1"):
            打开浏览器工具.find_element_by_id("J_SelectAll1").click()
            break
    except:
        print(f"找不到购买按钮")





while True:
    #获取电脑现在的时间,                       year month day
    当前时间 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # 对比时间，时间到的话就点击结算
    print(当前时间)
    if 当前时间 > 秒杀时间:
        # 点击结算按钮
        while True:
            try:
                if 打开浏览器工具.find_element_by_link_text("结 算"):
                    print("here")
                    打开浏览器工具.find_element_by_link_text("结 算").click()
                    print(f"主人,程序锁定商品,结算成功")
                    break
            except:
                pass
        while True:
            try:
                if 打开浏览器工具.find_element_by_link_text('提交订单'):
                    打开浏览器工具.find_element_by_link_text('提交订单').click()
                    print(f"抢购成功，请尽快付款")
            except:
                print(f"主人,结算提交成功,我已帮你抢到商品啦,请及时支付订单")
                speaker.Speak(f"主人,结算提交成功,我已帮你抢到商品啦,请及时支付订单")
                break
        time.sleep(0.01)