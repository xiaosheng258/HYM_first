"""
第4步,按照上一步的方式,绘制其他的样式的格子
"""

import tkinter as tk

# 设置行数和列数
Row = 20
Col = 12

# 设置每个格子的大小
cell_size = 30

# 设置窗口的高和宽
height = Row * cell_size
width = Col * cell_size

# 设置不同形状的格子
SHAPES = {
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S":[(-1, 0),(0, 0),(0, -1),(1, -1)],
    "T":[(-1, 0),(0, 0),(0, -1),(1, 0)],
    "I":[(0, 1),(0, 0),(0, -1),(0, -2)],
    "L":[(-1, 0),(0, 0),(-1, -1),(-1, -2)],
    "J":[(-1, 0),(0, 0),(0, 1),(0, -2)],
    "Z":[(-1, -1),(0, -1),(0, 0),(1, 0)]
}

# 设置格子的颜色
SHAPESCOLOR = {
    "O":"blue",
    "S":"red",
    "T":"yellow",
    "I":"green",
    "L":"purple",
    "J":"orange",
    "Z":"Cyan",
}

# 在画板上绘制格子
def draw_cell_background(canvas, col, row, color="#CCCCCC"):
    x0 = col * cell_size
    y0 = row * cell_size

    x1 = col * cell_size + cell_size
    y1 = row * cell_size + cell_size

    # 创建矩形
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)

def draw_blank_board(canvas):
    for ri in range(Row):
        for cj in range(Col):
            draw_cell_background(canvas, cj, ri)

def draw_cells(canvas, col, row, cell_list, color="#CCCCCC"):
    """
    :param canvas: 画板对象
    :param col: 这个形状的的原点所在的列
    :param row: 这个形状所的原点所在的行
    :param cell_list: 这个形状各个格子相对于自身的原点所处的位置坐标
    :param color: 这个形状的颜色
    :return:
    """
    for cell in cell_list:
        cell_col, cell_row = cell
        ci = cell_col + col
        ri = cell_row + row
        # 判断是否越界
        if 0 <= col < Col and 0 <= row < Row:
            draw_cell_background(canvas, ci, ri, color)

# 首先创建一个窗体
win = tk.Tk()

# 绘制画布的长宽
canvas = tk.Canvas(win, width=width, height=height)

# 打包放置组件对象
canvas.pack()

# 画背景
draw_blank_board(canvas)

# 开始画图形了， 这里是先测试一下
draw_cells(canvas, 3, 3, SHAPES['O'], SHAPESCOLOR['O'])
draw_cells(canvas, 3, 8, SHAPES['S'], SHAPESCOLOR['S'])
draw_cells(canvas, 3, 13, SHAPES['T'], SHAPESCOLOR['T'])
draw_cells(canvas, 8, 3, SHAPES['I'], SHAPESCOLOR['I'])
draw_cells(canvas, 8, 8, SHAPES['L'], SHAPESCOLOR['L'])
draw_cells(canvas, 8, 13, SHAPES['J'], SHAPESCOLOR['J'])
draw_cells(canvas, 5, 18, SHAPES['Z'], SHAPESCOLOR['Z'])


win.mainloop()
