import os
import sys
import time
import math
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import sign, get_direction, clear, WIDTH, HEIGHT
from objects import Creature
from item import Item

class ZoneGenerator:
    def __init__(self, width, height, temperature=5):
        self.width = width
        self.height = height
        self._temperature = temperature
        self.zone = None

    def _place_units(self):
        x_range = list(range(WIDTH))
        y_range = list(range(HEIGHT))
        for _ in range(50):
            x, y = random.choice(x_range), random.choice(y_range)
            if self.zone.get_tile_at(x, y).icon != '.':
                continue
            if len(self.zone.units) < WIDTH * HEIGHT // 200:
                self.zone.units.append(Creature(self.zone, 'cave bat', x, y, []))

    def _place_items(self):
        x_range = list(range(WIDTH))
        y_range = list(range(HEIGHT))
        for _ in range(50):
            x, y = random.choice(x_range), random.choice(y_range)
            if self.zone.get_tile_at(x, y).icon != '.':
                continue
            if len(self.zone.items) < WIDTH * HEIGHT // 200:
                name = random.choice(['hearty meal', 'stick', 'shovel'])
                self.zone.place_item(Item(name, x, y))

    def generate(self, stairs_up, stairs_down):
        raise NotImplementedError(self)

    # def fill(self, icon):
    #     self.grid = [list([icon]*self.width) for _ in range(self.height)]

    # def reset(self):
    #     self.fill('#')

    def seed(self, s):
        random.seed(s)

# if __name__ == '__main__':
#     gen = ZoneGenerator(65, 12, SnailGen, 5)
#     entrance = (55, 6)
#     exit = (6, 5)
#     gen.generate_zone(entrance, exit)
#     zone = gen.zone
#     zone.print(0)