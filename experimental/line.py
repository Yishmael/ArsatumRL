import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Loader, clear, get_direction, sign

from generators.zonegenerator import ZoneGenerator
from generators.zone import Zone
    
class LineGen(ZoneGenerator):
    def generate(self):
        grid = [list(['.']*self.width) for _ in range(self.height)]
        
        x1, y1 = 0, 0
        x2, y2 = 30, 20

        grid[y1][x1] = 'A'
        grid[y2][x2] = 'B'

        x, y = x1, y1
        dh = int(((x2 - x1)))
        dv = int(((y2 - y1)))
        r = (y2 - y1) / (x2 - x1)
        vertical = True
        if abs(r) < 1:
            vertical = False
            r = 1/r 
        change = round(r)
        change = round(r)
        rem = change % dh
        print(vertical, change, rem)
        # check if they differ more in x or in y 
        # if in y, use vertical lines, if x, use horizontal
        # calculate r, invert it if it's < 1
        # 
        # 

        i = 0
        h_count, v_count = 0, 0
        while True:
            dx, dy = get_direction((x, y), (x2, y2))
            if vertical:
                if v_count % change != 0:
                    dx = 0
                v_count += 1
            else:
                if h_count % change != 0:
                    dy = 0
                h_count += 1
            
            x, y = x + dx, y + dy
            if (x, y) == (x2, y2):
                break
            grid[y][x] = '#'
            i += 1

        print(dh, dv, r, i)


        self.zone = Zone(grid, [], [], self._temperature)

WIDTH, HEIGHT = 65, 52
if __name__ == '__main__':
    clear()
    gen = LineGen(WIDTH, HEIGHT)
    gen.generate()
    gen.zone.print()
