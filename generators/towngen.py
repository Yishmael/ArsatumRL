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
    

class TownGen(ZoneGenerator):
    def generate(self, stairs_down=None):
        # self.reset()
        file_id = 0
        files = ['town.txt', 'dungeon1.txt', 'dungeon2.txt', 'dungeon3.txt']
        grid = Loader.load_grid(files[file_id])
        # grid[stairs_down[1]][stairs_down[0]] = 'x'
        self.zone = Zone(grid, [], [], self._temperature)
        self.zone.recommended_stairs_coords.append((10, 5))
        # self._place_units()
        # self._place_items()

WIDTH, HEIGHT = 65, 12
if __name__ == '__main__':
    gen = TownGen(WIDTH, HEIGHT)
    clear()
    entrance = (55, 6)
    exit = (6, 5)
    # crawl_dir((0, 0), (0.1, 0.1, 0.1, 0.3), 100, 0.25)
    gen.generate(entrance)
    print_zone(gen.zone)
    # with open('../zones/dungeon3.txt', 'w') as f:
    #     f.write('\n'.join([''.join(row) for row in gen.grid]))
