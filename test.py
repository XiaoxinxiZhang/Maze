import time

class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.last_x, self.last_y = -1, -1  # 记录上一次小人位置

    def move_cursor(self, x, y):
        """移动光标到指定位置 (x, y)"""
        print(f"\033[{x + 1};{y + 1}H", end="")

    def print_state(self, x, y, path_marker=' ', wall_marker='@', person_marker='P'):
        """打印带玩家位置的迷宫状态"""
        if self.last_x != -1 and self.last_y != -1:
            # 清除上一次的小人位置
            self.move_cursor(self.last_x, self.last_y)
            print(path_marker if self.maze[self.last_x][self.last_y] == 1 else wall_marker, end="")

        # 更新小人位置
        self.move_cursor(x, y)
        print(person_marker, end="", flush=True)

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

# 模拟小人移动
m.print_state(1, 1)  # 初始位置
time.sleep(1)
m.print_state(1, 2)  # 向右移动
time.sleep(1)
m.print_state(2, 2)  # 向下移动