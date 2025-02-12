import time
import os
import random
import re


class Maze:
    """迷宫类，数据结构为列表套列表"""
    def __init__(self, width=10, height=10,
                 start_x=1, start_y=1,
                 p_edge=0.9, p_internal=0.3,
                 path_marker=' ', wall_marker='@'):
        """

        :param width: 宽度，即 len(maze)
        :param height: 高度，即 len(maze[0])
        :param start_x: 起点坐标 x
        :param start_y: 起点坐标 y
        :param p_edge: 边界为墙的概率
        :param p_internal: 内部墙的占比
        :param path_marker: 路的符号
        :param wall_marker: 墙的符号
        """
        self.width = width
        self.height = height
        self.start = (start_x, start_y)
        self.path_marker = path_marker
        self.wall_marker = wall_marker
        self.maze = self.generate_maze(start_x, start_y, p_edge, p_internal)
        self.print_maze(path_marker=path_marker, wall_marker=wall_marker)

    def generate_maze(self, start_x, start_y, p_edge=0.9, p_internal=0.3):
        """
        生成随机迷宫结构

        1代表路，2代表墙
        """

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

    def print_maze(self, path_marker=' ', wall_marker='@'):
        """打印迷宫"""
        os.system('cls')
        display = []
        for i, row in enumerate(self.maze):
            line = []
            for j, cell in enumerate(row):
                line.append(path_marker if cell == 1 else wall_marker)
            display.append(''.join(line))
        print('\n'.join(display))


class MazeSolver:
    """迷宫求解器"""

    # 每次可选择的方向
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, maze, person_marker='P'):
        """

        :param maze: 迷宫对象
        :param person_marker: 小人的符号
        """
        self.maze = maze
        self.person_marker = person_marker

        # 记录迷宫的某位置是否经过
        self.visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]

        # 记录上一次小人位置
        self.last_x, self.last_y = -1, -1

        # 记录小人走过的路径
        self.track = []

    def dfs(self, x, y):
        """深度优先搜索算法"""

        # 到达边界则成功
        if x == 0 or x == self.maze.height - 1 or y == 0 or y == self.maze.width - 1:
            self.track.append((x, y))
            self.print_state(x, y)
            return True

        self.visited[x][y] = True
        self.track.append((x, y))
        self.print_state(x, y)

        # 尝试四个方向
        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            if self.maze.is_valid(nx, ny) and not self.visited[nx][ny]:
                if self.dfs(nx, ny):
                    return True
                else:
                    # 回溯时清除错误路径
                    self._handle_backtracking(x, y)

        return False

    def print_state(self, x, y):
        """打印玩家的位置"""
        print(f"\033[{x + 1};{y + 1}H", end="")
        if self.last_x != -1 and self.last_y != -1:
            # 清除上一次的小人位置
            print(f"\033[{self.last_x + 1};{self.last_y + 1}H", end="")
            print(self.maze.path_marker, end="", flush=True)

        # 更新小人位置
        print(f"\033[{x + 1};{y + 1}H", end="")
        print(self.person_marker, end="", flush=True)

        # 记录当前小人位置
        self.last_x, self.last_y = x, y
        time.sleep(0.5)

    def _handle_backtracking(self, origin_x, origin_y):
        """处理回溯时的路径显示"""
        del self.track[-1]

        while self.track:
            last_pos = self.track.pop()
            self.print_state(*last_pos)
            if last_pos == (origin_x, origin_y):
                self.track.append(last_pos)
                break

    def show_result(self):
        """显示最终路径"""
        for i, (x, y) in enumerate(self.track):
            print(f"\033[{x + 1};{y + 1}H", end="")
            if i == 0:
                print('S', end="", flush=True)
            elif i == len(self.track) - 1:
                print('E', end="", flush=True)
            else:
                print('.', end="", flush=True)

    def run(self):
        """执行搜索算法"""
        if self.dfs(*self.maze.start):
            print(f"\033[{self.maze.height + 1};{self.maze.width + 1}H", end='')
            print("\nSuccess!")
            solver.show_result()
        else:
            print(f"\033[{self.maze.height + 1};{self.maze.width + 1}H", end='')
            print("\nNo solution found!")

        print(f"\033[{self.maze.height + 1};{self.maze.width + 1}H", end='')
        input("\n\nPress any key to exit...")


if __name__ == '__main__':
    # 初始化迷宫和求解器
    str_hw = input("Create a maze, and the size is (height x width): ")
    r1 = re.match(r"^\D*(\d+)(?# 迷宫的高度)"
                  r"\D+(?# 中间的任意字符)"
                  r"(\d+)\D*$(?# 迷宫的宽度)", str_hw).groups()
    h, w = int(r1[0]), int(r1[1])

    str_xy = input("Creat a person,and the position of (x , y):")
    r2 = re.match(r"^\D*(\d+)(?# 横坐标)"
                  r".+(?# 中间的任意字符)"
                  r"(\d+)\D*$(?# 纵坐标)", str_xy).groups()
    x, y = int(r2[0]), int(r2[1])

    os.system("cls")
    print(f"Maze size: {h} x {w}; Start Point: ({x} , {y})")
    time.sleep(3)

    maze = Maze(height=h, width=w, start_x=x, start_y=y)

    solver = MazeSolver(maze)

    solver.run()
