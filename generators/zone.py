import random

from utils import distance_between_points, clear, get_icon, WIDTH, HEIGHT
from generators.staircase import Staircase
from objects import Creature
from item import Item

class Zone:
    def __init__(self, grid, units=[], items=[], temperature=5):
        self._grid = grid
        self.units = units
        self._items = items
        self.temperature = temperature
        self.staircases = []
        self.id = 0
        self.recommended_stairs_coords = []
        self._messages = []

    def get_recommended_stairs_coords(self):
        for recomm in self.recommended_stairs_coords:
            self.recommended_stairs_coords.remove(recomm)
            return recomm
        
        locs = []
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.get_tile_at(x, y).terrain_icon != '#':
                    if not self.get_staircase_at(x, y):
                        locs.append((x, y))
        x, y = random.choice(locs)
        return x, y

    def init(self):
        for item in self.items:
            item.temperature = self.temperature

    def __repr__(self):
        return f'Zone-{self.id}'

    @property
    def player(self):
        for unit in self.units:
            if unit.icon == '@':
                return unit
        return None
        
    def place_unit_by_name(self, unit_name, x, y, items=[]):
        self.units.append(Creature(self, unit_name, x, y, items))

    @property
    def items(self):
        return self._items
    
    def place_item(self, item, reset_temperature=True):
        if reset_temperature:
            item.temperature = self.temperature
        self.items.append(item)
        items = self.get_items_in_range(item.x, item.y, 0)
        for item1 in items:
            for item2 in items:
                item1.affect_item(item2)

    def tick(self):
        for unit in self.units:
            unit.update_temperature(self.temperature)
        for item in list(self.items):
            item.update_temperature(self.temperature)
            if item.broken:
                pieces = item.pieces
                for piece in pieces:
                    piece.x, piece.y = item.x, item.y
                    self.items.append(piece)
                self.items.remove(item)

    def cleanup(self):
        for unit in list(self.units):
            if unit.destroyed:
                self.units.remove(unit)
        for item in list(self.items):
            if item.destroyed:
                self.items.remove(item)

    def get_items_in_range(self, x, y, distance):
        items = []
        for item in self.items:
            if distance_between_points((x, y), (item.x, item.y)) <= distance:
                items.append(item)
        return items

    def get_units_in_range(self, x, y, distance):
        units = []
        for unit in self.units:
            if distance_between_points((x, y), (unit.x, unit.y)) <= distance:
                units.append(unit)
        return units

    def get_tile_at(self, x, y):
        tile = Tile(self.temperature)
        for unit in self.units:
            if (unit.x, unit.y) == (x, y):
                tile.units.append(unit)
        
        for item in self.items:
            if (item.x, item.y) == (x, y):
                tile.items.append(item)

        for staircase in self.staircases:
            if (staircase.x1, staircase.y1) == (x, y):
                tile.staircase = staircase

        tile.terrain_icon = self._grid[y][x]
        tile.icon = tile.terrain_icon
        if tile.staircase:
            tile.icon = tile.staircase.get_icon(self.id)
        if tile.items:
            tile.icon = tile.items[0].icon
        if tile.units:
            tile.icon = tile.units[0].icon

        tile.walkable = tile.terrain_icon == '.' and not tile.units

        return tile

    def get_grid(self):
        return self._grid

    def get_staircase_at(self, x, y):
        for s in self.staircases:
            if (x, y) == (s.x1, s.y1):
                return s
        return None
    
    def add_message(self, message):
        self._messages.append(message)

    def get_messages(self):
        messages = list(self._messages)
        self._messages.clear()
        return messages

    def print(self, cls=False):
        if cls:
            clear()
        for idx, row in enumerate(self._grid):
            row = list(row)
            for staircase in self.staircases:
                x, y = staircase.x1, staircase.y1
                if y == idx:
                    row[x] = staircase.get_icon(self.id)
            for item in self.items:
                x, y = item.x, item.y
                if y == idx:
                    row[x] = item.icon
            for ent in self.units:
                x, y = ent.x, ent.y
                if y == idx:
                    row[x] = ent.icon
            print(''.join(row))
    
class Tile:
    def __init__(self, temperature):
        self.temperature = temperature
        self.walkable = False
        self.staircase = None
        self.units = []
        self.items = []
        self.terrain_icon = ''
        self.icon = ''
        