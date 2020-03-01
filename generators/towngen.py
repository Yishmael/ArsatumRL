import math
import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Loader, clear, get_direction, sign, WIDTH, HEIGHT

if __name__ == '__main__':
    from zonegenerator import ZoneGenerator
    from zone import Zone
    from boxgen import Box
else:
    from generators.zonegenerator import ZoneGenerator
    from generators.zone import Zone
    from generators.boxgen import Box

from item import Item

class TownGen(ZoneGenerator):
    def generate(self):
        # self.reset()
        file_id = 0
        files = ['town.txt', 'dungeon1.txt', 'dungeon2.txt', 'dungeon3.txt']
        grid = Loader.load_grid(files[file_id])
        grid.extend(['.'*self.width]*(self.height-len(grid)))
        for row in grid:
            if len(row) < self.width:
                row.extend('.'*(self.width-len(row)))

        self.zone = Zone(grid, [], [], self._temperature)
        self.zone.recommended_stairs_coords.append((10, 5))
        
        self.zone.place_unit_by_name('white rat', 22, 7, [Item(i) for i in ['cotton sweater']])
        self.zone.place_item(Item('hearty meal', 22, 10))
        self.zone.place_unit_by_name('coyote', 32, 2)
        self.zone.place_unit_by_name('coyote', 33, 2)
        self.zone.place_item(Item('stick', 33, 3))
        self.zone.place_unit_by_name('coyote', 34, 2)
        self.zone.place_unit_by_name('coyote', 35, 2)
        self.zone.place_item(Item('hearty meal', 12, 4))
        self.zone.place_item(Item('barrel top', 12, 3))
        self.zone.place_item(Item('glass flask', 18, 5))
        self.zone.place_item(Item('glass shard', 16, 8))
        self.zone.place_item(Item('glass shard', 16, 9))
        self.zone.place_item(Item('glass shard', 16, 10))
        # self.zone.place_item(Item('pebble', 27, 4))

        # self.zone.place_item(Item('motivation'), 55, 10)

if __name__ == '__main__':
    WIDTH, HEIGHT = 65, 12
    clear()
    gen = TownGen(WIDTH, HEIGHT)
    gen.generate()
    gen.zone.print()
    # with open('../zones/dungeon3.txt', 'w') as f:
    #     f.write('\n'.join([''.join(row) for row in gen.grid]))
