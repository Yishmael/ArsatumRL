import os
import sys
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import sign, distance_between_points
from statistics import stdev

from loader import Loader

width = 65
height = 12

def print_table(table):
    print('\n'.join(''.join(str(p) for p in row) for row in table))

def get_patches(n):
    table = [list('#' for _ in range(width)) for _ in range(height)]
    points = []
    for i in range(n):
        p = (random.randint(0, width-1), random.randint(0, height-1))
        points.append(p)
        x, y = p[0], p[1]
        vert = 3
        hori = 4
        
        for i in range(hori):
            for j in range(vert):
                if x+i >= len(table[y]):
                    break
                if y+j >= len(table):
                    break
                table[y+j][x+i] = '.'
                table[y+j][x+i] = '.'
    return table

def fill(x, y):
    start = (x, y)
    table[start[1]][start[0]] = '.'
    for _ in range(height):
        for y in range(height):
            for x in range(width):
                if table[y][x] != '|':
                    continue
                if x+1 < width:
                    if table[y][x+1] == '.': table[y][x] = '.'
                if x-1 >= 0:
                    if table[y][x-1] == '.': table[y][x] = '.'
                if y-1 >= 0:
                    if table[y-1][x] == '.': table[y][x] = '.'
                if y+1 < height:
                    if table[y+1][x] == '.': table[y][x] = '.'

os.system('cls')

grid = [list(' ' if random.randint(0, 1) > 0 else 0 for _ in range(width)) for _ in range(height)]
#grid = [list(i%1 for i in range(width)) for _ in range(height)]
#print('\n'.join(''.join([str(p) for p in row]) for row in grid))

table = [list('#' for _ in range(width)) for _ in range(height)]
table = [list(' ' for _ in range(width)) for _ in range(height)]

height = len(grid)
width = len(grid[0])

#table = get_patches(80)
#rooms = [(4, 5), (50, 10), (25, 2), (16, 2)]
rooms = []
attempt_count = 0
while len(rooms) < 3:
    new = (random.randint(5, width-4), random.randint(2, height-3))
    for room in rooms:
        if distance_between_points(room, new) < 10:
            attempt_count += 1
            break
    else:
        rooms.append(new)
    if attempt_count > 5:
        break

for room in rooms:
    px, py = room
    for y in range(height):
        for x in range(width):
            if abs(px - x) <= 3 and abs(py - y) <= 3:
                if px in (x-3, x+3) or py in (y-3, y+3):
                    table[y][x] = '#'
   
for idx, room in enumerate(rooms):
    x, y = room
    table[y][x] = idx

for idx, room in enumerate(rooms):
    if idx == len(rooms)-1:
        break
    x, y = room
    xx, yy = rooms[idx+1]
    i, j = x, y
    while True:
        dx, dy = sign(xx-i), sign(yy-j)
        if x > 1 and x < width - 1 and y > 1 and y < height - 1:
            if random.random() < 0.8:
                i += dx
            if random.random() < 0.2:
                j += dy
        table[j][i] = '.'
        if abs(xx-i) < 2 and abs(yy-j) < 2:
            break
    print_table(table)


#fill(0, 3)
#print_table(table)

def gen_patches(n):
    table = get_patches(n)
    print(n)
    print_table(table)
#[gen_patches(n) for n in range(40, 60, 3)]