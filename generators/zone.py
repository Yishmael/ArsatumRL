from utils import print_zone
from generators.staircase import Staircase

class Zone:
    def __init__(self, grid, units=[], items=[], temperature=5):
        self._grid = grid
        self.units = units
        self.items = items
        self.temperature = temperature
        self.staircases = []
        self.id = 0
        self.recommended_stairs_coords = []

    #TODO make indexing everything at that tile, not just terrain from grid
    # def __getitem__(self, y):
        # return self.grid[y]

    def __repr__(self):
        return f'Zone-{self.id}'
        
    def print(self, cls=True):
        print_zone(self, cls)
        
    def place_unit(self, unit_name, x, y):
        self.units.append((unit_name, x, y))
        
    def place_item(self, item_name, x, y):
        self.items.append((item_name, x, y))

    def get_tile_at(self, x, y):
        return self._grid[y][x]

    def get_grid(self): 
        return self._grid

    # TODO remove this after removing old worldgenerator
    def get_staircases_coords(self):
        s = []
        for y, row in enumerate(self._grid):
            for icon in ['x']:
                if icon in row:
                    for x in [x for x, e in enumerate(row) if e == icon]:
                        s.append((icon, x, y))
        return s

    def update(self):
        for s in self.staircases:
            x, y = s.x1, s.y1
            self._grid[y][x] = s.get_icon(self.id)