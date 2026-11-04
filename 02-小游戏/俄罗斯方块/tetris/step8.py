"""
第8步:实现俄罗斯方块图标的旋转
"""
import tkinter as tk
import random

# 设置行数和列数
Row = 20
Col = 12

# 设置格子的刷新频率，单位是毫秒
FPS = 250

# 设置每个格子的大小
cell_size = 30

# 设置窗口的高和宽
height = Row * cell_size
width = Col * cell_size

# 设置不同形状的格子
SHAPES = {
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)]
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

# 绘制板块
def draw_blank_board(canvas):
    for ri in range(Row):
        for cj in range(Col):
            draw_cell_background(canvas, cj, ri)

# 绘制单元格
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

block_list = []
for i in range(Row):
    i_row = ['' for j in range(Col)]
    block_list.append(i_row)


# 开始画图形了， 这里是先测试一下
# draw_cells(canvas, 3, 3, SHAPES['O'], SHAPESCOLOR['O'])
# draw_cells(canvas, 3, 8, SHAPES['S'], SHAPESCOLOR['S'])
# draw_cells(canvas, 3, 13, SHAPES['T'], SHAPESCOLOR['T'])
# draw_cells(canvas, 8, 3, SHAPES['I'], SHAPESCOLOR['I'])
# draw_cells(canvas, 8, 8, SHAPES['L'], SHAPESCOLOR['L'])
# draw_cells(canvas, 8, 13, SHAPES['J'], SHAPESCOLOR['J'])
# draw_cells(canvas, 5, 18, SHAPES['Z'], SHAPESCOLOR['Z'])


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

# 测试代码
# draw_block_move(canvas, one_block)

def product_new_block():
    # 随机生成新的俄罗斯方块
    kind = random.choice(list(SHAPES.keys()))

    cr = [Col // 2, 0]
    new_block = {
        "kind": kind,
        "cell_list": SHAPES[kind],
        'cr': cr
    }
    return new_block

def check_move(block, direction=[0,0]):
    """
    :param block:俄罗斯方块的前身
    :param direction: 移动方向
    :return: boolean 是否可以朝着指定的方向移动
    """
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc + direction[0]
        r = cell_r + cr + direction[1]

        # 判断边界
        if c < 0 or c >= Col or r >= Row:
            return False
        # r >= 0是防止格子下不来的情况
        if r >= 0 and block_list[r][c]:
            return False
    return True

# 保存当前的俄罗斯方块到列表里面
def save_to_block_list(block):
    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr

        block_list[r][c] = shape_type


def horizontal_move_block(event):
    """
    左右水平移动俄罗斯方块
    event:键盘的监听事件
    """
    # 这里只设置了左右两个方向
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        draw_block_move(canvas, current_block, direction)


def rotate_block(event):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    rotate_list = []
    for cell in cell_list:
        cell_c, cell_r = cell
        rotate_cell = [cell_r, -cell_c]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        'kind': current_block['kind'],  # 对应俄罗斯方块的类型
        'cell_list': rotate_list,
        'cr': current_block['cr']
    }

    if check_move(block_after_rotate):
        cc, cr = current_block['cr']
        draw_cells(canvas, cc, cr, current_block['cell_list'])
        draw_cells(canvas, cc, cr, rotate_list, SHAPESCOLOR[current_block['kind']])
        current_block = block_after_rotate


def land(event):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    cc, cr = current_block['cr']
    min_height = Row
    for cell in cell_list:
        cell_c, cell_r = cell
        c, r = cell_c + cc, cell_r + cr
        if block_list[r][c]:
            return
        h = 0
        for ri in range(r + 1, Row):
            if block_list[ri][c]:
                break
            else:
                h += 1
        if h < min_height:
            min_height = h

    down = [0, min_height]
    if check_move(current_block, down):
        draw_block_move(canvas, current_block, down)


# 让游戏不断循环 通过递归实现
def game_loop():
    win.update()

    global current_block
    # 如果当前没有俄罗斯方块 产生一个新的
    if current_block is None:
        # 生成新的俄罗斯方块
        new_block = product_new_block()
        draw_block_move(canvas, new_block)
        current_block = new_block
    # 如果当前有了就往下走
    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
        else:
            # 保存当前的俄罗斯方块
            save_to_block_list(current_block)
            current_block = None
    win.after(FPS, game_loop) # 注意的是这个game_loop后面不能加括号

# 当前的俄罗斯方块
current_block = None

# 画布聚焦
canvas.focus_set()
# 添加左右移动的事件
canvas.bind("<KeyPress-Left>", horizontal_move_block)
canvas.bind("<KeyPress-Right>", horizontal_move_block)
# 添加变化角度的事件
canvas.bind("<KeyPress-Up>", rotate_block)
canvas.bind("<KeyPress-Down>", land)


game_loop()
win.mainloop()
