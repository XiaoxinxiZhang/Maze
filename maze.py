import time
import os
import random


class Maze:
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, width=10, height=10, start_x=1, start_y=1, p_edge=0.9, p_internal=0.3):
        self.width = width
        self.height = height
        self.start = (start_x, start_y)
        self.maze = self.generate_maze(start_x, start_y, p_edge, p_internal)

    def generate_maze(self, start_x, start_y, p_edge=0.9, p_internal=0.3):
        """生成随机迷宫结构"""

        # 初始化全为路的迷宫
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # 边界生成随机墙，默认概率为 90%
        for i in range(self.height):
            for j in range(self.width):
                if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                    maze[i][j] = random.choices([1, 0], weights=[1 - p_edge, p_edge])[0]

        # 内部添加随机障碍，默认其中 30% 为障碍
        for _ in range(int((self.height - 2) * (self.width - 2) * p_internal)):
            r_x = random.randint(1, self.height - 2)
            r_y = random.randint(1, self.width - 2)
            maze[r_x][r_y] = 0

        # 确保起点畅通
        maze[start_x][start_y] = 1
        return maze

    def is_valid(self, x, y):
        """检查位置是否可通行"""
        return 0 <= x < self.height and 0 <= y < self.width and self.maze[x][y] == 1

    def print_state(self, x, y, path_marker=' ', wall_marker='@', person_marker='P'):
        """打印带玩家位置的迷宫状态"""
        os.system('cls')
        display = []
        for i, row in enumerate(self.maze):
            line = []
            for j, cell in enumerate(row):
                if (i, j) == (x, y):
                    line.append(person_marker)
                elif cell == 1:
                    line.append(path_marker)
                elif cell == 0:
                    line.append(wall_marker)
            display.append(''.join(line))
        print('\n'.join(display))
        time.sleep(0.5)


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]
        self.track = []

    def dfs(self, x, y):
        """深度优先搜索算法"""
        # 到达边界则成功
        if x == 0 or x == self.maze.height - 1 or y == 0 or y == self.maze.width - 1:
            self.track.append((x, y))
            self.maze.print_state(x, y)
            return True

        self.visited[x][y] = True
        self.track.append((x, y))
        self.maze.print_state(x, y)

        # 尝试四个方向
        for dx, dy in Maze.DIRECTIONS:
            nx, ny = x + dx, y + dy
            if self.maze.is_valid(nx, ny) and not self.visited[nx][ny]:
                if self.dfs(nx, ny):
                    return True
                else:
                    # 回溯时清除错误路径
                    self._handle_backtracking(x, y)

        return False

    def _handle_backtracking(self, origin_x, origin_y):
        """处理回溯时的路径显示"""
        while self.track:
            last_pos = self.track.pop()
            self.maze.print_state(*last_pos)
            if last_pos == (origin_x, origin_y):
                self.track.append(last_pos)
                break

    def show_result(self):
        """显示最终路径"""
        path_marker = {}
        for i, (x, y) in enumerate(self.track):
            if i == 0:
                path_marker[(x, y)] = 'S'
            elif i == len(self.track) - 1:
                path_marker[(x, y)] = 'E'
            else:
                path_marker[(x, y)] = '.'
        self.maze.print_state(-1, -1, path_marker)  # 使用无效坐标触发全图显示


if __name__ == '__main__':
    # 初始化迷宫和求解器
    h = int(input("请输入迷宫的高度："))
    w = int(input("请输入迷宫的宽度："))
    sx = int(input(f"请输入小人的起点 x 坐标 [0,{h - 1})："))
    sy = int(input(f"请输入小人的起点 y 坐标 [0,{w - 1})："))

    os.system("cls")
    print(f"Maze size: {h} x {w}; Start Point: ({sx} , {sy})")
    time.sleep(3)

    maze = Maze(height=h, width=w, start_x=sx, start_y=sy)
    solver = MazeSolver(maze)

    # 执行搜索算法
    if solver.dfs(*maze.start):
        print("\nSuccess! Path:")
        solver.show_result()
    else:
        print("\nNo solution found!")

    os.system("pause")
