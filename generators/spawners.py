import os
import sys
import random

from generators.zone import Zone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from objects import Creature
from item import Item

class Spawner:
    def __init__(self, density=1):
        self.density = density
    
    def spawn_units(self, zone: Zone):
        x_range = list(range(zone.width))
        y_range = list(range(zone.height))
        for _ in range(50):
            x, y = random.choice(x_range), random.choice(y_range)
            if zone.get_tile_at(x, y).icon != '.':
                continue
            if len(zone.units) < zone.width * zone.height * self.density // 200 :
                zone.units.append(Creature(zone, 'cave bat', x, y, []))

    def spawn_items(self, zone: Zone):
        x_range = list(range(zone.width))
        y_range = list(range(zone.height))
        for _ in range(50):
            x, y = random.choice(x_range), random.choice(y_range)
            if zone.get_tile_at(x, y).icon != '.':
                continue
            if len(zone.items) < zone.width * zone.height * self.density // 200:
                name = random.choice(['hearty meal', 'stick', 'stick', 'shovel'])
                zone.place_item(Item(name, x, y))