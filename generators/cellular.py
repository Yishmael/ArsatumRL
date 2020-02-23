import os
import sys
import time
import math
import random
from itertools import combinations, permutations
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
            tile = '.'
            grid[i][j] = tile

clear()
reset()
for i in range(HEIGHT):
    for j in range(WIDTH):
        if random.random() < 0.3:
            tile = '#'
            grid[i][j] = tile

directions = list(set(permutations([-1, -1, -1, 0, 0, 0, 1, 1, 1], 2)))
directions.remove((0, 0))
pr()
print()
old = grid
for _ in range(5):
    old = [list(row) for row in grid]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] != '.':
                continue
            neighbors = []
            for d in directions:
                dx, dy = d
                if y+dy < 0 or y+dy >= len(grid) or x+dx < 0 or x+dx >= len(grid[0]):
                    continue
                tile = old[y+dy][x+dx]
                neighbors.append(tile)
            count = neighbors.count('#')
            if count >= 4:
                grid[y][x] = '#'
            
pr()