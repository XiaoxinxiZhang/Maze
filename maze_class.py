import time
import os
import random


class Maze:
    """迷宫类，小人在其中走"""

    """迷宫的类属性"""

    # 定义四个方向：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, size_x, size_y,
                 start_x=1, start_y=1,
                 wall_sign='@', road_sign=' ', person_sign='P'):
        """

        :param size_x: 迷宫的宽度
        :param size_y: 迷宫的长度
        :param start_x: 小人的起始点，左上角为(0,0)
        :param start_y:
        :param wall_sign: 墙的符号
        :param road_sign: 路的符号
        :param person_sign: 小人的符号
        """
        self.size_x = size_x
        self.size_y = size_y
        self.start_x = start_x
        self.start_y = start_y
        self.wall_sign = wall_sign
        self.road_sign = road_sign
        self.person_sign = person_sign
        self.data = [[' '] * size_y for _ in range(size_x)]

    def generate(self, p_wall_edge=0.9, p_wall_inside=0.3):
        """
        随机初始化迷宫，起点为路
        默认四周为有 90% 的概率为墙，中间有 10% 的概率为墙
        :return: None
        """

        for i in range(self.size_x):
            for j in range(self.size_y):
                if i == 0 or i == self.size_x - 1 or j == 0 or j == self.size_y - 1:
                    self.data[i][j] = \
                    random.choices([self.wall_sign, self.road_sign], weights=[p_wall_edge, 1 - p_wall_edge])[0]
                else:
                    self.data[i][j] = random.choices([self.wall_sign,
                                                      self.road_sign],
                                                     weights=[p_wall_inside, 1 - p_wall_inside])[0]
        # 确保起点为路径
        self.data[self.start_x][self.start_y] = self.road_sign

    def is_valid(self, x, y):
        """
        判断当前位置是否在迷宫范围内，且为路径
        :param x: 迷宫纵坐标 [0,size_x-1)
        :param y: 迷宫横坐标 [0,size_y-1)
        :return: True or False
        """
        return 0 <= x < self.size_x - 1 \
            and 0 <= y < self.size_y - 1 \
            and self.data[x][y] == self.road_sign

    def print_maze(self, x, y, t):
        """

        :param x: 小人当前纵坐标
        :param y: 小人当前横坐标
        :param t: 打印后的等待时间
        :return: None
        """
        # 清除屏幕
        # os.system('cls')

        # 创建一个临时的迷宫副本，转化为字符表示
        maze_copy = self.data.copy()

        # 将多个位置
        maze_copy[x][y] = self.person_sign

        # 打印迷宫
        for row in maze_copy:
            print(''.join(row))
        time.sleep(t)

        # # 深度优先搜索
    # def dfs(x, y, visited):
    #     global track
    #     # 如果当前点在迷宫外围且是路，获胜
    #     if x == 0 or x == n - 1 or y == 0 or y == m - 1:
    #         print_maze(maze, x, y)  # 打印当前状态
    #         track.append([x, y])
    #         return True
    #
    #     visited[x][y] = True  # 标记当前位置为已访问
    #     print_maze(maze, x, y)  # 打印当前状态
    #     track.append([x, y])
    #
    #     # 探索四个方向
    #     for dx, dy in directions:
    #         nx, ny = x + dx, y + dy
    #         if is_valid(nx, ny) and not visited[nx][ny]:
    #             if dfs(nx, ny, visited):
    #                 return True  # 如果找到了成功路径，返回True
    #             else:
    #                 del track[-1]
    #                 while True:
    #                     if not track:
    #                         break
    #                     xy = track.pop()
    #                     print_maze(maze, xy[0], xy[1])  # 打印当前状态
    #                     if xy[0] == x and xy[1] == y:
    #                         track.append(xy)
    #                         break
    #
    #     return False  # 如果四个方向都无法找到路径，返回False


if __name__ == '__main__':
    m = Maze(10, 10)

    # 随机生成迷宫
    m.generate()

    if m.is_valid(2, 2):
        m.print_maze(2, 2, 1)

    # # 假设小人的起点是(1, 1)
    # start_x, start_y = 1, 1
    #
    # # 随机生成迷宫
    # maze = generate_maze(10, 10, start_x, start_x)
    #
    # # 创建一个访问记录的数组
    # visited = [[False for _ in range(m)] for _ in range(n)]
    #
    # # 调用深度优先搜索
    # if dfs(start_x, start_y, visited):
    #     print("\nsuccess!\n\nTrack:\n")
    #     # 创建一个临时的迷宫副本，转化为字符表示
    #     maze_copy = []
    #     for row in maze:
    #         maze_copy.append([' ' if cell == 1 else '@' for cell in row])  # ' '为路径，'@'为墙
    #     for i, xy in enumerate(track):
    #         if i == 0:
    #             maze_copy[xy[0]][xy[1]] = 'S'
    #         elif i == len(track) - 1:
    #             maze_copy[xy[0]][xy[1]] = 'E'
    #         else:
    #             maze_copy[xy[0]][xy[1]] = '.'
    #     for row in maze_copy:
    #         print(''.join(row))
    # else:
    #     print("\nlose!")
