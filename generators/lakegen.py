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

clear()
reset()

lake = (20, 5)

for _ in range(10):
    reset()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if math.hypot(lake[0]-x, (lake[1]-y)*2) < 6:
                grid[y][x] = '~'
            if math.hypot(lake[0]-x, (lake[1]-y)*2) < 4:
                if random.random() < 0.1:
                    grid[y][x] = '-'
    pr(1)
    time.sleep(.5)
