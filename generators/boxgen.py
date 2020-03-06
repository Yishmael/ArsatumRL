import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generators.zone import Zone
from generators.zonegenerator import ZoneGenerator
from utils import HEIGHT, WIDTH, Vector, clear, get_direction


class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.icon = '#'
        self.door = Vector()

    def __repr__(self):
        return f'({self.x},{self.y})'

    @property
    def center(self):
        return Vector(self.x + self.w//2, self.y + self.h//2)

    def contains(self, x, y):
        return self.x <= x <= self.x + self.w and \
            self.y <= y <= self.y + self.h

    def touches(self, x, y):
        return self.x <= x <= self.x + self.w and y in [self.y, self.y+self.h] or \
            self.y <= y <= self.y + self.h and x in [self.x, self.x + self.w]

    def get_walls(self, allow_edges=False):
        walls = []
        for x in range(self.x, self.x + self.w + 1):
            for y in range(self.y, self.y + self.h + 1):
                if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
                    continue
                if self.touches(x, y):
                    if not allow_edges:
                        if (x, y) in [(self.x, self.y), (self.x + self.w, self.y), 
                                      (self.x, self.y + self.h), (self.x + self.w, self.y + self.h)]:
                            continue
                    walls.append(Vector(x, y))
        return walls

    def get_wall(self, allow_edges=False):
        walls = self.get_walls(allow_edges)
        return random.choice(walls)

    def get_icon(self, x, y):
        for wall in self.get_walls(True):
            if wall == Vector(x, y):
                if self.door == wall:
                    return '.'
        return '#'

    def intersects(self, box: 'Box'):
        if box.y + box.h < self.y or box.x + box.w < self.x or \
            self.y + self.h < box.y or self.x + self.w < box.x:
            return False
        return True

    def apply_on(self, grid):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.touches(x, y):
                    grid[y][x] = self.icon
                elif self.contains(x, y):
                    grid[y][x] = '.'

    
class BoxGen(ZoneGenerator):
    def generate(self):
        # random.seed(12)
        grid = [list([' ']*self.width) for _ in range(self.height)]
        max_width = 30
        max_height = 10
        boxes = [Box(random.randint(0, WIDTH-max_width), random.randint(0, HEIGHT-max_height),
                     random.randint(7, max_width), random.randint(4, max_height)) for _ in range(30)]
        for box1 in list(boxes):
            for box2 in list(boxes):
                if box1 is not box2:
                    if box1.intersects(box2):
                        if box1 in boxes:
                            # continue
                            boxes.remove(box1)

        for box in boxes:
            box.apply_on(grid)
        
        for box1, box2 in zip(boxes, boxes[1:]):
            x, y = box1.center.x, box1.center.y
            while True:
                dx, dy = get_direction((x, y), (box2.center.x, box2.center.y))
                if random.random() < 0.5:
                    dx = 0
                else:
                    dy = 0
                x, y = x + dx, y + dy
                grid[y][x] = '.'
                if box2.touches(x, y):
                    break

        # border
        for y in range(1, HEIGHT - 1):
            for x in range(1, WIDTH - 1):
                if grid[y][x] == ' ':
                    if '.' in [grid[y-1][x], grid[y+1][x], grid[y][x-1], grid[y][x+1],
                               grid[y-1][x-1], grid[y-1][x+1], grid[y+1][x-1], grid[y+1][x+1]]:
                        grid[y][x] = '#'

                
        self.zone = Zone(grid, [], [], self._temperature)

if __name__ == '__main__':
    WIDTH, HEIGHT = 165, 40
    # WIDTH, HEIGHT = 65, 42
    clear()
    gen = BoxGen(WIDTH, HEIGHT)
    gen.generate()
    gen.zone.print()
