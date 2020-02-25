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

from item import Item

class TownGen(ZoneGenerator):
    def generate(self, stairs_down=None):
        # self.reset()
        file_id = 0
        files = ['town.txt', 'dungeon1.txt', 'dungeon2.txt', 'dungeon3.txt']
        grid = Loader.load_grid(files[file_id])
        # grid[stairs_down[1]][stairs_down[0]] = 'x'
        self.zone = Zone(grid, [], [], self._temperature)
        self.zone.recommended_stairs_coords.append((10, 5))
        
        self.zone.place_unit_by_name('white rat', 22, 7)# [Item(i) for i in ['cotton sweater']])
        self.zone.place_unit_by_name('coyote', 32, 2)
        self.zone.place_unit_by_name('coyote', 33, 2)
        self.zone.place_unit_by_name('coyote', 34, 2)
        self.zone.place_unit_by_name('coyote', 35, 2)
        self.zone.place_item(Item('hearty meal', 12, 4))
        self.zone.place_item(Item('barrel top', 12, 3))
        self.zone.place_item(Item('glass flask', 18, 5))
        # world.place(Item('pebble'), 27, 4, 0)

        # self.zone.place_item(Item('motivation'), 55, 10)

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
