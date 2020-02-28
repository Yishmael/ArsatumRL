import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Loader, clear, get_direction, sign

if __name__ == '__main__':
    from zonegenerator import ZoneGenerator
    from zone import Zone
else:
    from generators.zonegenerator import ZoneGenerator
    from generators.zone import Zone
    
class BlankGen(ZoneGenerator):
    def generate(self):
        grid = [list(['.']*self.width) for _ in range(self.height)]
        self.zone = Zone(grid, [], [], self._temperature)

WIDTH, HEIGHT = 65, 12
if __name__ == '__main__':
    clear()
    gen = BlankGen(WIDTH, HEIGHT)
    gen.generate()
    gen.zone.print()
