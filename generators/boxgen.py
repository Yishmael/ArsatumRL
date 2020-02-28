import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, Vector, get_direction

if __name__ == '__main__':
    from zonegenerator import ZoneGenerator
    from zone import Zone
else:
    from generators.zonegenerator import ZoneGenerator
    from generators.zone import Zone

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

    def contains(self, x, y):
        return self.x <= x <= self.x + self.w and \
            self.y <= y <= self.y + self.h

    def touches(self, x, y):
        return self.x <= x <= self.x + self.w and y in [self.y, self.y+self.h] or \
            self.y <= y <= self.y + self.h and x in [self.x, self.x + self.w]

    def get_walls(self, allow_edges=False):
        l = []
        for x in range(self.x, self.x + self.w + 1):
            for y in range(self.y, self.y + self.h + 1):
                if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
                    continue
                if self.touches(x, y):
                    if not allow_edges:
                        if (x, y) in [(self.x, self.y), (self.x + self.w, self.y), 
                                      (self.x, self.y + self.h), (self.x + self.w, self.y + self.h)]:
                            continue
                    l.append(Vector(x, y))
        return l

    def get_wall(self, allow_edges=False):
        l = self.get_walls(allow_edges)
        return random.choice(l)

    def intersects(self, box: 'Box'):
        if box.y + box.h < self.y or box.x + box.w < self.x or \
            self.y + self.h < box.y or self.x + self.w < box.x:
            return False
        return True       
    
class BoxGen(ZoneGenerator):
    def generate(self):
        random.seed(10)
        grid = [list(['.']*self.width) for _ in range(self.height)]
        boxes = [Box(2 + random.randint(0, WIDTH-10), random.randint(0, HEIGHT-5), 
                random.randint(6, 10), random.randint(3, 5)) for _ in range(20)]

        for box1 in list(boxes):
            for box2 in list(boxes):
                if box1 is not box2:
                    if box1.intersects(box2):
                        if box1 in boxes:
                            # continue
                            boxes.remove(box1)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                for box in boxes[:]:
                    if box.touches(x, y):
                        grid[y][x] = box.icon

        for box in boxes:
            x, y = box.get_wall()
            grid[y][x] = '+'
            box.door = Vector(x, y)
        
        # for box1, box2 in zip(boxes, boxes[1:]):
        #     door1 = box1.door
        #     door2 = box2.door
        #     x, y = door1.x, door1.y
        #     while True:
        #         dx, dy = get_direction((x, y), (door2.x, door2.y))
        #         x, y = x + dx, y + dy
        #         grid[y][x] = 'x'
        #         if (x, y) == (door2.x, door2.y):
        #             break
                
        self.zone = Zone(grid, [], [], self._temperature)

WIDTH, HEIGHT = 65, 42
if __name__ == '__main__':
    clear()
    gen = BoxGen(WIDTH, HEIGHT)
    gen.generate()
    gen.zone.print()