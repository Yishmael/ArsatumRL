import os
import time

from utils import get_direction

class Entity:
    def __init__(self, x, y, icon):
        self.x = x
        self.y = y
        self.icon = icon
        self.head = False
    def __repr__(self):
        return '{} ({},{})'.format(self.icon, self.x, self.y)

def pr():
    os.system('cls')
    for idx, row in enumerate(grid):
        row = list(row)
        for entity in entities:
            x, y = entity.x, entity.y
            if y == idx:
                row[x] = entity.icon
        print(''.join(row))

def get_snake_locs(size):
    snake = []
    for i in range(size):
        if i < 4:
            pos = (i, 0)
            x = i
            snake.append(pos)
        elif 4 <= i < 6:
            pos = (x, i-3)
            snake.append(pos)
    return snake

def form_snake(snake_locs):
    for _ in range(50):
        done = 0
        for idx, (ent, snake_loc) in enumerate(zip(entities, snake_locs)):
            if idx == 0:
                ent.head = True
            direction = get_direction((ent.x, ent.y), (center_x+snake_loc[0], center_y+snake_loc[1]))
            if direction == (0, 0): # NOTE add this kind of comparison
                done += 1
                continue
            ent.x += direction.x
            ent.y += direction.y
        if done == len(entities):
            return


WIDTH, HEIGHT = 50, 12

grid = [list('.')*WIDTH for _ in range(HEIGHT)]

entities = [Entity(5, 1, '0'), Entity(10, 1, '1'), Entity(15, 1, '2'), Entity(20, 1, '3'), 
            Entity(25, 3, '4'), Entity(30, 3, '5')]

center_x, center_y = 0, 0
for ent in entities:
    center_x += ent.x
    center_y += ent.y
center_x = int(center_x /len(entities))
center_y = int(center_y / len(entities))
snake_locs = get_snake_locs(len(entities))
form_snake(snake_locs)

pr()