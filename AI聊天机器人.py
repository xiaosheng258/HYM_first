# # 导入语音播报库
# import pyttsx3
#
# # 初始化对象
# talker = pyttsx3.init()
# # 创建一个用户名玉米，用户密码321
# userName = "玉米"
# userPass = "321"
# print("欢迎使用AI聊天机器人！")
# # 把演讲稿给talker对象
# talker.say("欢迎使用聊天机器人！")
# # 启动
# talker.runAndWait()
#
# # input输入函数，提示用户输入账号密码
# talker.say("请输入你的账号和密码")
# talker.runAndWait()
# inputName = input("请输入你的账号：")
# inputPass = input("请输入你的密码：")
#
# print(inputName, inputPass)
#
#
# # 判断用户输入的账号和电脑中保存的账号是否一致
# if inputName == userName and inputPass == userPass:
#     print("登录成功！")
#     talker.say("恭喜你登陆成功！")
#     talker.say("想和我聊点什么吗？")
#     talker.runAndWait()
#
#     # 循环
#     while True:
#
#         # 接收用户输入的问题
#         question = input(inputName + "请输入你的问题: ")
#         # 针对问题做出解答，strip()函数：对字符串进行处理
#         answer = question.strip("吗？？" + "!")
#         if question == "不聊了拜拜":
#             talker.say("好的，拜拜就拜拜！")
#             talker.runAndWait()
#             print("机器人的回答：好的，拜拜就拜拜！")
#             break
#         print("机器人的回答：" + answer)
#         talker.say(answer)
#         talker.runAndWait()
# else: # 否则
#     print("登录失败！")
#     talker.say("账号或密码错误，很遗憾登录失败")
#     talker.runAndWait()


import pygame
import requests






