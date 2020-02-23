import os
import sys
import time
import math
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import sign, get_direction, clear, distance_between_points

WIDTH, HEIGHT = 65, 12
# WIDTH, HEIGHT = 80, 30
# WIDTH, HEIGHT = 165, 40
grid = [list(['.']*WIDTH) for _ in range(HEIGHT)]

def pr(cls=False):
    if cls:
        clear()
    for row in grid:
        print(''.join(row))

def reset():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            grid[i][j] = '.'

def make_grid(line):
    ''' Create rectangular areas.'''
    x1, y1, x2, y2 = line
    space = 2 + 1
    vertical = x1 == x2
    dist = distance_between_points((x1, y1), (x2, y2))
    if dist < space:
        return
    if vertical: # draw horizontal lines
        if y1 >= y2:
            return
        if y2 - y1 < 2*space:
            return
        # east
        y = random.randint(y1+space, y2-space)
        x = x1
        if x+1 < WIDTH:
            for xx in range(x+1, WIDTH):
                if grid[y][xx] != '.':
                    break
                grid[y][xx] = '#'
            line = (x+1, y, xx, y)
            make_grid(line)
        # west
        y = random.randint(y1+space, y2-space)
        x = x1
        if 0 < x-1+1:
            for xx in reversed(range(0, x-1+1)):
                if grid[y][xx] != '.':
                    break
                grid[y][xx] = '#'
            line = (xx, y, x-1, y)
            make_grid(line)
    else: # draw vertical lines
        if x1 >= x2:
            return
        if x2 - x1 < 2*space:
            return
        # south
        x = random.randint(x1+space, x2-space)
        y = y1
        if y+1 < HEIGHT:
            for yy in range(y+1, HEIGHT):
                if grid[yy][x] != '.':
                    break
                grid[yy][x] = '#'
            line = (x, y+1, x, yy)
            make_grid(line)
        # north
        x = random.randint(x1+space, x2-space)
        y = y1
        if 0 < y-1+1:
            for yy in reversed(range(0, y-1+1)):
                if grid[yy][x] != '.':
                    break
                grid[yy][x] = '#'
            line = (x, yy, x, y-1)
            make_grid(line)            

clear()
x1, y1 = random.randint(0, WIDTH-1), 0
x2, y2 = x1, HEIGHT - 1
for y in range(y1, y2+1):
    grid[y][x1] = '#'
make_grid((x1, y1, x2, y2))
pr()
reset()
# with open('../areas/dungeon4.txt', 'w') as f:
#     f.write('\n'.join([''.join(row) for row in grid]))
