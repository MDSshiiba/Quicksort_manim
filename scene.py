from manim import *
import random
from random import seed, uniform
import colorama
from collections import deque

S = []
def qSort(startNum, endNum,seq):
    pivot = seq[(startNum + endNum) // 2]
    left = startNum
    right = endNum

    while True:
        while seq[left] < pivot:
            left += 1
        while pivot < seq[right]:
            right -= 1
        if left >= right:
            break

        seq[left],seq[right] = seq[right],seq[left]
        S.append([left,right])

        left += 1
        right -= 1

    if startNum < left-1:
        qSort(startNum, left-1,seq)
    if right + 1 < endNum:
        qSort(right+1, endNum,seq)

def bubble_sort(seq):
    n = len(seq) - 1
    for i in range(n):
        for j in range(n - i):
            if seq[j] > seq[j+1]:
                seq[j] , seq[j+1] = seq[j+1], seq[j]
                yield (j,j+1)

class SortAnimation(Scene):
    def construct(self):
        g = Group()
        numbers = list(range(1,11))
        random.shuffle(numbers)
        print(numbers)
        for number in numbers:
            g.add(Circle(radius=number/2*0.1))

        self.add(g.arrange_in_grid(rows=1,col_widths=[1]*10))
	# 追加分↓
        qSort(0, len(numbers)-1,numbers)
        A = list(range(11))
        a = []
        for i,j in S:
            A[i],A[j] = A[j],A[i]
            a.append([A[i],A[j]])
        print(*a)
        for i,j in a:
            self.play(Swap(g.submobjects[i], g.submobjects[j]))
            #g.submobjects[i], g.submobjects[i+1] = g.submobjects[i+1], g.submobjects[i]
        print(S)

class MazeByMakingWall():
    """ 壁伸ばし方で迷路を作る。"""
    def __init__(self, width, height):
        """ 迷路全体を構成する2次元配列、迷路の外周を壁とし、それ以外を通路とする。"""

        self.PATH = 0
        self.WALL = 1

        self.width = width
        self.height = height
        self.maze = []
        # 壁を作り始める開始ポイントを保持しておくリスト。
        self.lst_cell_start_make_wall = []
        # 迷路は、幅高さ5以上の奇数で生成する。
        if(self.height < 5 or self.width < 5):
            print('at least 5')
            exit()
        if (self.width % 2) == 0:
            self.width += 1
        if (self.height % 2) == 0:
            self.height += 1
        for x in range(0, self.width):
            row = []
            for y in range(0, self.height):
                if (x == 0 or y == 0 or x == self.width-1 or y == self.height -1):
                    cell = self.WALL
                else:
                    cell = self.PATH
                    # xyとも偶数の場合は、壁を作り始める開始ポイントとして保持。
                    if (x % 2 == 0 and y % 2 == 0):
                        self.lst_cell_start_make_wall.append([x, y])
                row.append(cell)
            self.maze.append(row)
            # スタートとゴールを入れる。
        self.maze[1][1] = 'S'
        self.maze[width-2][height-2] = 'G'
    def make_maze(self):
        """ 迷路の配列を作り戻す """
        # 壁の拡張を開始できるセルがなくなるまでループする。
        while self.lst_cell_start_make_wall != []:
            # 開始セルをランダムに取得してリストからは削除。
            x_start, y_start = self.lst_cell_start_make_wall.pop(random.randrange(0, len(self.lst_cell_start_make_wall)))
            # 選択候補が通路の場合は壁の拡張を開始する。
            if self.maze[x_start][y_start] == self.PATH:
                # 拡張中の壁情報を保存しておくリスト。
                self.lst_current_wall = []
                self.extend_wall(x_start, y_start)
        return self.maze
    def extend_wall(self, x, y):
        """ 開始位置から壁を2つずつ伸ばす """
        # 壁を伸ばすことのできる方向を決める。通路かつ、その2つ先が現在拡張中の壁ではない。
        lst_direction = []
        if self.maze[x][y-1] == self.PATH and [x, y-2] not in self.lst_current_wall:
            lst_direction.append('up')
        if self.maze[x+1][y] == self.PATH and [x+2, y] not in self.lst_current_wall:
            lst_direction.append('right')
        if self.maze[x][y+1] == self.PATH and [x, y+2] not in self.lst_current_wall:
            lst_direction.append('down')
        if self.maze[x-1][y] == self.PATH and [x-2, y] not in self.lst_current_wall:
            lst_direction.append('left')
        #壁を伸ばせる方向がある場合
        if lst_direction != []:
            #まずはこの地点を壁にして、拡張中の壁のリストに入れる。
            self.maze[x][y] = self.WALL
            self.lst_current_wall.append([x, y])
            # 伸ばす方向をランダムに決める
            direction = random.choice(lst_direction)
            # 伸ばす2つ先の方向が通路の場合は、既存の壁に到達できていないので、拡張を続ける判断のフラグ。
            contineu_make_wall = False
            # 伸ばした方向を壁にする
            if direction == 'up':
                contineu_make_wall = (self.maze[x][y-2] == self.PATH)
                self.maze[x][y-1] = self.WALL
                self.maze[x][y-2] = self.WALL
                self.lst_current_wall.append([x, y-2])
                if contineu_make_wall:
                    self.extend_wall(x, y-2)
            if direction == 'right':
                contineu_make_wall = (self.maze[x+2][y] == self.PATH)
                self.maze[x+1][y] = self.WALL
                self.maze[x+2][y] = self.WALL
                self.lst_current_wall.append([x+2, y])
                if contineu_make_wall:
                    self.extend_wall(x+2, y)
            if direction == 'down':
                contineu_make_wall = (self.maze[x][y+2] == self.PATH)
                self.maze[x][y+1] = self.WALL
                self.maze[x][y+2] = self.WALL
                self.lst_current_wall.append([x, y+2])
                if contineu_make_wall:
                    self.extend_wall(x, y+2)
            if direction == 'left':
                contineu_make_wall = (self.maze[x-2][y] == self.PATH)
                self.maze[x-1][y] = self.WALL
                self.maze[x-2][y] = self.WALL
                self.lst_current_wall.append([x-2, y])
                if contineu_make_wall:
                    self.extend_wall(x-2, y)
        else:
            previous_point_x, previous_point_y = self.lst_current_wall.pop()
            self.extend_wall(previous_point_x, previous_point_y)

    def print_maze(self):
        """ 壁が色付きの迷路を出力する。"""
        colorama.init()
        for row in self.maze:
            for cell in row:
                if cell == self.PATH:
                    print('   ', end='')
                elif cell == self.WALL:
                    print(termcolor.colored('   ', 'green', 'on_green'), end='')
                elif cell == 'S':
                    print(termcolor.colored('STA', 'red'), end='')
                elif cell == 'G':
                    print(termcolor.colored('GOA', 'red'), end='')
            print()

maze = MazeByMakingWall(15, 15)
maze_list = maze.make_maze()
print(maze_list)
cnt = 0
goal = [0,0]
for i in range(len(maze_list)):
    for j in range(len(maze_list[i])):
        if maze_list[i][j] == 'G':
            cnt += 1
            goal = [i,j]
if cnt == 0:
    exit()
class MazeSolving(Scene):
    def construct(self):
        vg = VGroup()
        start = [0,0]
        goal = [0,0]
        for i in range(len(maze_list)):
            for j in range(len(maze_list[i])):
                if maze_list[i][j] == 'S':
                    start[0],start[1] = i,j
                    vg.add(Circle(radius=0.1, color=PURE_GREEN, fill_opacity=1))
                elif maze_list[i][j] == 'G':
                    goal[0],goal[1] = i,j
                    vg.add(Circle(radius=0.1, color=RED,fill_opacity=1))
                elif maze_list[i][j] == 1:
                    vg.add(Circle(radius=0.1, color=BLACK))
                else:
                    vg.add(Circle(radius=0.1, color=WHITE))
        vg.arrange_in_grid()
        self.play(vg.animate)
        start_text = Text("Start",font_size=24)
        start_text.next_to(vg[start[0]*len(maze_list)+start[1]],LEFT*0.5,buff=0.5)
        self.play(start_text.animate,run_time=0.1)
        goal_text = Text("Goal",font_size=24)
        goal_text.next_to(vg[goal[0]*len(maze_list)+goal[1]],RIGHT*0.5,buff=0.5)
        self.play(goal_text.animate,run_time=0.1)
        #BFS
        MAX = 10**2
        visited = [[-1]*len(maze_list) for _ in range(len(maze_list[0]))]
        d = deque()
        for i in range(len(maze_list)):
            for j in range(len(maze_list[i])):
                if maze_list[i][j] != 1:
                    visited[i][j] = MAX
                if maze_list[i][j] == 'S':
                    visited[i][j] = 0
                    d.append([i,j])
        next = [[0,1],[0,-1],[1,0],[-1,0]]
        while d:
            now = d.popleft()
            if (now != goal):
                self.play(vg[now[0]*len(maze_list)+now[1]].animate.set_fill(GREEN, opacity=1),run_time=0.1)
            for i,j in next:
                if (0 <= (now[0]+i)) and ((now[0]+i) < len(maze_list)) and (0 <= (now[1]+j)) and ((now[1]+j) < len(maze_list[0])):
                    if (maze_list[now[0]+i][now[1]+j] != 1) and (visited[now[0]+i][now[1]+j] < MAX):
                        visited[now[0]][now[1]] = min(visited[now[0]][now[1]],visited[now[0]+i][now[1]+j]+1)
                    if (maze_list[now[0]+i][now[1]+j] == 0) and (visited[now[0]+i][now[1]+j] == MAX):
                        d.append([now[0]+i,now[1]+j])
                    elif (maze_list[now[0]+i][now[1]+j] == 'G') and (visited[now[0]+i][now[1]+j] == MAX):
                        d.append([now[0]+i,now[1]+j])
            if maze_list[now[0]][now[1]] == 'G':
                number = Integer(visited[now[0]][now[1]])
                number.next_to(vg[now[0]*len(maze_list)+now[1]],DOWN*0.5,buff=0.5)
                self.play(number.animate,run_time=0.1)
                d.clear()
        print(visited[goal[0]][goal[1]])
        d.append([goal[0],goal[1]])
        roots = [[1]*len(maze_list) for _ in range(len(maze_list[0]))]
        roots[start[0]][start[1]] = 0
        roots[goal[0]][goal[1]] = 0
        while d:
            now = d.popleft()
            if visited[goal[0]][goal[1]] > visited[now[0]][now[1]] > 0:
                roots[now[0]][now[1]] = 0
                self.play(vg[now[0]*len(maze_list)+now[1]].animate.set_fill(GOLD, opacity=1),run_time=0)
            for i,j in next:
                if (visited[now[0]][now[1]] == (visited[now[0]+i][now[1]+j] + 1)) and (visited[now[0]][now[1]] > 1):
                    d.append([now[0]+i,now[1]+j])
                    break
        for i in range(len(maze_list)):
            for j in range(len(maze_list[0])):
                if roots[i][j]:
                    self.play(vg[i*len(maze_list)+j].animate.set_color(BLACK),run_time=0)
        self.wait(5)
