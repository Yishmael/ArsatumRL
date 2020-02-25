from utils import print_zone, distance_between_points
from generators.staircase import Staircase
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

    #TODO make indexing everything at that tile, not just terrain from grid
    # def __getitem__(self, y):
        # return self.grid[y]

    @property
    def player(self):
        for unit in self.units:
            if unit.icon == '@':
                return unit
        return None
        
    def __repr__(self):
        return f'Zone-{self.id}'

    def init(self):
        for item in self._items:
            item.temperature = self.temperature
        
    def print(self, cls=True):
        print_zone(self, cls)
        
    def place_unit_by_name(self, unit_name, x, y):
        self.units.append((unit_name, x, y))

    @property
    def items(self):
        return self._items
    
    def place_item(self, item, reset_temperature=True):
        item.temperature = self.temperature
        self._items.append(item)

    def get_tile_at(self, x, y):
        return self._grid[y][x]

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

    def tick(self):
        for unit in self.units:
            unit.update_temperature(self.temperature)
        for item in self._items:
            item.update_temperature(self.temperature)

    # TODO remove this after removing old worldgenerator
    def get_staircases_coords(self):
        s = []
        for y, row in enumerate(self._grid):
            for icon in ['x']:
                if icon in row:
                    for x in [x for x, e in enumerate(row) if e == icon]:
                        s.append((icon, x, y))
        return s

    def get_items_in_range(self, x, y, distance):
        items = []
        for item in self.items:
            if distance_between_points((x, y), (item.x, item.y)) <= distance:
                items.append(item)
        return items