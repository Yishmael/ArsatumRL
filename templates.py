'''Generate a zone with rooms, items, objects, and tiles.'''
class ZoneGenerator:
    '''Use specified generator to create terrain.'''
    def __init__(self, generator_type, temperature):
        pass
    def _place_units(self):
        pass
    def _place_items(self):
        pass
    def _prettify(self):
        pass
    def generate_zone(self):
        pass

'''Generates a world consisting of zones and connects them.'''
class WorldGenerator:
    def _connect_zones(self):
        pass
    def generate_world(self):
        pass

'''Info on all units, ground items, tiles in the zone, and coordinates of all starcases.'''
class Zone:
    def __init__(self, grid, units=[], items=[], temperature=5):
        pass
    def place_unit(self, unit, x, y):
        pass
    def place_item(self, item, x, y):
        pass    

'''Info on the zone and position to move to once triggered.'''
class Staircase:
    def __init__(self, zone_id1, x1, y1, zone_id2, x2, y2):
        pass
    def get_exit_location(self, zone_id):
        pass

'''Info on whether or not a tile was explored and is it walkable.'''
class Tile:
    def __init__(self, icon, walkable):
        pass

'''Contains the zones, and changes them when needed.'''
class World:
    '''Once a request to change zone is made, the position of the player is read and 
    new player coordinates for the next zone are obtained from the current zone.'''
    def change_zone(self):
        pass

'''Main game container.'''
class Window:
    '''Check all opened windows, current zone, update the display buffer, and print it.'''
    def draw(self):
        pass
    '''Add messages to be displayed on the next update/draw.'''
    def add_message(self, text):
        pass        
    '''Modify the full-screen table for display.''' 
    def update_display(self):
        pass

class Item:
    def __init__(self, name, icon, actions, select_text):
        pass

class Inventory:
    def __init__(self):
        pass
    '''Perform an action based on the key pressed.'''
    def do_action(self, key):
        pass
    def _drop_item(self, item):
        pass
    def _use_item(self, item):
        pass
