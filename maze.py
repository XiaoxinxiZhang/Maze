import curses
import time

class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.last_x, self.last_y = -1, -1

    def print_state(self, stdscr, x, y, path_marker=' ', wall_marker='@', person_marker='P'):
        """打印带玩家位置的迷宫状态"""
        if self.last_x != -1 and self.last_y != -1:
            # 清除上一次的小人位置
            stdscr.addch(self.last_x, self.last_y, path_marker if self.maze[self.last_x][self.last_y] == 1 else wall_marker)

        # 更新小人位置
        stdscr.addch(x, y, person_marker)
        stdscr.refresh()

        # 记录当前小人位置
        self.last_x, self.last_y = x, y
        time.sleep(0.5)

# 示例迷宫
maze = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

# 初始化迷宫对象
m = Maze(maze)

# 使用 curses 运行
def main(stdscr):
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()
    m.print_state(stdscr, 1, 1)  # 初始位置
    time.sleep(1)
    m.print_state(stdscr, 1, 2)  # 向右移动
    time.sleep(1)
    m.print_state(stdscr, 2, 2)  # 向下移动

curses.wrapper(main)