import pyautogui    # 操作窗体
from pynput.keyboard import Key, Controller     # 操作键盘
import time     # 操作时间

content = input("您要轰炸的内容：")
times = eval(input("您要轰炸的次数："))

pyautogui.hotkey('ctrl', 'alt', 'w')

# 键盘操作对象
keyboard = Controller()
for i in range(times):
    keyboard.type(content)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)     # 间隔0.1s
