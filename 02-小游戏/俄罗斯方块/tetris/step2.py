"""
第2步:画格子,用tkinter里面Canvas功能
"""

import tkinter as tk

# 设置行数和列数
row = 20
col = 12

# 设置每个格子的大小
cell_size = 30

# 设置窗口的高和宽
height = row * cell_size
width = col * cell_size

# 首先创建一个窗体
win = tk.Tk()

# 在画板上绘制格子
def draw_cell(canvas, col, row, color="#CCCCCC"):
    x0 = col * cell_size
    y0 = row * cell_size

    x1 = col * cell_size + cell_size
    y1 = row * cell_size + cell_size

    # 创建矩形
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)

def draw_blank_board(canvas):
    for ri in range(row):
        for cj in range(col):
            draw_cell(canvas, cj, ri)


# 绘制画布的长宽
canvas = tk.Canvas(win, width=width, height=height)

# 打包放置组件对象
canvas.pack()

# 绘制画板
draw_blank_board(canvas)

# 程序循环执行
win.mainloop()
