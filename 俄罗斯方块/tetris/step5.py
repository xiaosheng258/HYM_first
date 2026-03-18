"""
第5步:让俄罗斯方块图标动起来
本质是设置一个刷新时间，然后这个格子不断的加载，然后不断的刷新画面,得到一种动态累积的效果

"""

import tkinter as tk
import time
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


# 设置格子的刷新频率，单位是毫秒
FPS = 500

# 定义让俄罗斯方块移动的方法
def draw_block_move(canvas, block, direction=[0,0]):
    """
    :param canvas: 面板对象
    :param block: 俄罗斯方块
    :param direction: 移动的方向
    :return:
    """
    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']

    draw_cells(canvas, c, r, cell_list)

    dc, dr = direction
    new_c, new_r = c + dc, r + dr
    block['cr'] = [new_c, new_r]
    draw_cells(canvas, new_c, new_r, cell_list, SHAPESCOLOR[shape_type])

# 用字典定义每个形状的属性
one_block = {
    'kind': 'O', # 对应俄罗斯方块的类型
    'cell_list': SHAPES['O'], # 对应的每个俄罗斯方块的坐标
    'cr': [3, 3], # 对应的行列坐标
}

draw_block_move(canvas, one_block)

# 让游戏不断循环 通过递归实现
def game_loop():
    win.update()

    # 往下走
    down = [0, 1]
    draw_block_move(canvas, one_block, down)
    win.after(FPS, game_loop)  # 注意的是这个game_loop后面不能加括号

game_loop()
win.mainloop()
