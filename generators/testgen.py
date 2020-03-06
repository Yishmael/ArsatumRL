import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Loader, clear, get_direction, sign, Vector, distance_between_points
from generators.zonegenerator import ZoneGenerator
from generators.zone import Zone
    
class TestGen(ZoneGenerator):
    def generate(self):
        grid = [list(['#']*self.width) for _ in range(self.height)]
        grids = []
        # random.seed(2)

        c = Vector(self.width*2//4, self.height+3)
        size = 2
        for idx, door in enumerate([
                                    Vector(c.x - size, c.y - size - 5),
                                    Vector(c.x + size, c.y - size - 5),
                                    Vector(c.x + 0, c.y - size//2 - 5),
                                    Vector(c.x - size, c.y - size//2 - 5),
                                    ]):
            grid = [list(['#']*self.width) for _ in range(self.height)]
            holes = [door]
            for y in range(self.height):
                for x in range(self.width):
                    if distance_between_points((c.x, c.y), (x, y)) <= size:
                        grid[y][x] = '.'
                    elif random.random() < 0.2:
                        grid[y][x] = '.'
                        holes.append(Vector(x, y))

            if idx % 2 == 0:
                holes = sorted(holes, key=lambda h: (distance_between_points((h.x, h.y), (door.x, door.y)), h.y, 0))
            else:
                holes = sorted(holes, key=lambda h: (distance_between_points((h.x, h.y), (door.x, door.y)), h.y, -h.x))
            new_holes = [holes[0]]
            for hole in holes[1:]:
                if hole.y < new_holes[-1].y:
                    new_holes.append(hole)
            holes = new_holes
            
            grid[door.y][door.x] = '+'
            for hole in holes:
                x, y = hole
                grid[y][x] = '+'

            path = []
            for prev, curr in zip(holes, holes[1:]):
                x, y = prev
                while True:
                    dx, dy = get_direction((x, y), (curr.x, curr.y))
                    if grid[y + dy][x + dx] == '+':
                        break
                    
                    if dx != 0 and dy != 0: # diagonal
                        if random.random() < 0.5:
                            dx = 0
                        else:
                            dy = 0
                    grid[y + dy][x + dx] = '.'
                    path.append(Vector(x + dx, y + dy))
                    x += dx
                    y += dy
                    
            for y in range(self.height):
                for x in range(self.width):
                    if grid[y][x] == '.':
                        if Vector(x, y) not in path:
                            if (x > c.x + size or x < c.x - size) or (y > c.y + size or y < c.y - size):
                                # not in room
                                grid[y][x] = '#'
                    elif grid[y][x] == '+':
                        grid[y][x] = '.'
            grids.append(grid)
    
        for y in range(self.height):
            for x in range(self.width):
                if '.' in [g[y][x] for g in grids]:
                    grid[y][x] = '.'        

        self.zone = Zone(grid, [], [], self._temperature)

WIDTH, HEIGHT = 65, 42
# WIDTH, HEIGHT = 165, 40
if __name__ == '__main__':
    clear()
    gen = TestGen(WIDTH, HEIGHT)
    gen.generate()
    gen.zone.print()
