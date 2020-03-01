import os
import sys
import time
import math
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import sign, get_direction, clear

if __name__ == '__main__':
    from zonegenerator import ZoneGenerator
    from zone import Zone
else:
    from generators.zonegenerator import ZoneGenerator
    from generators.zone import Zone

class SnailGen(ZoneGenerator):
    def generate(self, chance=0.2, exponent=0.5, diagonals=False):
        # self._generator.generate(stairs_up, stairs_down, 0.2, 0.5, False)
        ''' Crawl from start and go toward a point.'''
        # self.fill('.')
        grid = [list(['#']*self.width) for _ in range(self.height)]
        for _ in range(3):
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            stairs_up = (random.randint(0, self.width//3), random.randint(0, self.height//3))
            stairs_down = (random.randint(self.width*2//3+1, self.width-1), random.randint(self.height*2//3+1, self.height-1))
            current = tuple(stairs_up)
            grid[current[1]][current[0]] = '<'
            grid[stairs_down[1]][stairs_down[0]] = '>'
            holes = 0
            org_chance = chance
            while True:
                dx, dy = random.choice(dirs)
                scale = math.hypot(stairs_down[0]-current[0], stairs_down[1]-current[1]) / math.hypot(self.width, self.height)
                chance = org_chance * scale**exponent
                chance = max(0.05, chance)
                if random.random() < chance:
                    dx = get_direction(current, stairs_down).x
                if random.random() < chance:
                    dy = get_direction(current, stairs_down).y
                if not diagonals and dx != 0 and dy != 0:
                    if random.random() < 0.5:
                        dx = 0
                    else:
                        dy = 0
                        
                if current[0]+dx < 0 or current[0]+dx >= len(grid[0]) or \
                current[1]+dy < 0 or current[1]+dy >= len(grid):
                    continue
                current = (current[0]+dx, current[1]+dy)
                if grid[current[1]][current[0]] not in ['.']:
                    if current == stairs_down:
                        break
                    grid[current[1]][current[0]] = '.'
                    holes += 1
                else:
                    continue
            grid[stairs_up[1]][stairs_up[0]] = '.'
            grid[stairs_down[1]][stairs_down[0]] = '.'

        self.zone = Zone(grid, [], [], self._temperature)
        self.zone.recommended_stairs_coords = [tuple(stairs_up), tuple(stairs_down)]
        self._place_units()
        self._place_items()

if __name__ == '__main__':
    gen = SnailGen(65,12)
    clear()
    # entrance = (55, 6)
    # exit = (6, 5)
    # crawl_dir((0, 0), (0.1, 0.1, 0.1, 0.3), 100, 0.25)
    gen.generate(0.2, 0.5)
    gen.zone.print()
    # with open('../zones/dungeon3.txt', 'w') as f:
    #     f.write('\n'.join([''.join(row) for row in gen.zone.get_grid()]))
