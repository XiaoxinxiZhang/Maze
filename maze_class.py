import time
import os
import random


class Maze:
    """迷宫类，小人在其中走"""

    """迷宫的类属性"""
    # 定义四个方向：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, m, n, start_x=1, start_y=1, wall_sign='@', road_sign=' '):
        pass


# 随机生成迷宫
def generate_maze(m, n, start_x, start_y):
    # 初始化迷宫周围全为墙，中间全为路
    maze = [[1 for _ in range(m)] for _ in range(n)]

    for i in range(m):
        for j in range(n):
            if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                maze[i][j] = random.choices([1, 0], weights=[0.1, 0.9])[0]

    for i in range(int(m * n * 0.3)):
        r_x = random.randint(0, m - 1)
        r_y = random.randint(0, n - 1)
        maze[r_x][r_y] = 0
    # 确保起点为路径
    maze[start_x][start_y] = 1

    return maze


# 判断当前位置是否在迷宫范围内且是路径
def is_valid(x, y):
    return 0 <= x < n and 0 <= y < m and maze[x][y] == 1


# 打印当前的迷宫状态
def print_maze(maze, x, y):
    # 清除屏幕
    os.system('cls' if os.name == 'nt' else 'clear')

    # 创建一个临时的迷宫副本，转化为字符表示
    maze_copy = []
    for row in maze:
        maze_copy.append([' ' if cell == 1 else '@' for cell in row])  # ' '为路径，'@'为墙
    maze_copy[x][y] = 'P'  # 将小人位置标记为'P'

    # 打印迷宫
    for row in maze_copy:
        print(''.join(row))
    time.sleep(1)  # 暂停0.5秒，让每步显示清晰


# 深度优先搜索
def dfs(x, y, visited):
    global track
    # 如果当前点在迷宫外围且是路，获胜
    if x == 0 or x == n - 1 or y == 0 or y == m - 1:
        print_maze(maze, x, y)  # 打印当前状态
        track.append([x, y])
        return True

    visited[x][y] = True  # 标记当前位置为已访问
    print_maze(maze, x, y)  # 打印当前状态
    track.append([x, y])

    # 探索四个方向
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and not visited[nx][ny]:
            if dfs(nx, ny, visited):
                return True  # 如果找到了成功路径，返回True
            else:
                del track[-1]
                while True:
                    if not track:
                        break
                    xy = track.pop()
                    print_maze(maze, xy[0], xy[1])  # 打印当前状态
                    if xy[0] == x and xy[1] == y:
                        track.append(xy)
                        break

    return False  # 如果四个方向都无法找到路径，返回False


if __name__ == '__main__':
    # 假设小人的起点是(1, 1)
    start_x, start_y = 1, 1

    # 随机生成迷宫
    maze = generate_maze(10, 10, start_x, start_x)

    # 创建一个访问记录的数组
    visited = [[False for _ in range(m)] for _ in range(n)]

    # 调用深度优先搜索
    if dfs(start_x, start_y, visited):
        print("\nsuccess!\n\nTrack:\n")
        # 创建一个临时的迷宫副本，转化为字符表示
        maze_copy = []
        for row in maze:
            maze_copy.append([' ' if cell == 1 else '@' for cell in row])  # ' '为路径，'@'为墙
        for i, xy in enumerate(track):
            if i == 0:
                maze_copy[xy[0]][xy[1]] = 'S'
            elif i == len(track) - 1:
                maze_copy[xy[0]][xy[1]] = 'E'
            else:
                maze_copy[xy[0]][xy[1]] = '.'
        for row in maze_copy:
            print(''.join(row))
    else:
        print("\nlose!")
