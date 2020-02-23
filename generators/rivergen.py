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
line_y = [4, 5, 6]
river = (15, 50)
river_len = river[1] - river[0] + 1
for y in line_y:
    for x in river:
        grid[y][x] = '#'
wave_space = 5
num_waves = int(river_len/wave_space)

y = 5
dashes = wave_space-1
wave = '-'*dashes + '~'
for _ in range(10):
    for y in line_y:
        for x in range(river_len):
            grid[y][x + river[0]] = wave[x % len(wave)]
    pr(1)
    time.sleep(0.7 / wave_space)
    wave = wave[len(wave)-1:] + wave[:len(wave)-1]
