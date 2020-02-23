import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Loader, clear, get_direction, print_zone, sign

if __name__ == '__main__':
    from zonegenerator import ZoneGenerator
    from zone import Zone
else:
    from generators.zonegenerator import ZoneGenerator
    from generators.zone import Zone
    
class BlankGen(ZoneGenerator):
    def generate(self, c):
        grid = [list(['.']*self.width) for _ in range(self.height)]
        for i in range(c):
            grid[self.height-1][i] = str(c)
        self.zone = Zone(grid, [], [], self._temperature)

WIDTH, HEIGHT = 65, 12
if __name__ == '__main__':
    gen = BlankGen(WIDTH, HEIGHT)
    clear()
    gen.generate(1)
    print_zone(gen.zone)
