import random

from .pane import Pane
from utils import get_dir
from item import Item

class State:
    DEFAULT = 0
    ITEM_SELECTED = 1
    ITEM_USED = 2

class Inventory(Pane):
    def __init__(self, unit, items=[]):
        super(Inventory, self).__init__(32, 8)
        self.unit = unit
        self._items = list(items)
        self.shown = False
        self.state = State.DEFAULT
        self.selected_item = None
        self.scroll_y = 0

    def __repr__(self):
        return ', '.join(item.name for item in self._items)

    def add_item(self, item):
        self._items.append(item)

    def add_items(self, items):
        for item in items:
            self.add_item(item)

    def is_empty(self):
        return len(self._items) == 0

    def recv(self, message):
        command, value = message.split()
        if command == 'refill':
            for item in self._items:
                if item.refillable() and not item.full():
                    name = item.name
                    item.fill(value)
                    self.unit.zone.add_message(f'You fill {name} with {value}.')
                    break
            else:
                self.unit.zone.add_message('You wash your face in the fountain.')
    
    @property
    def items(self):
        return self._items

    @property
    def mass(self):
        return 2 + sum(item.mass for item in self._items)

    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2

        title = f'Backpack ({self.mass:.1f} kg)'
        display[1][left:left+len(title)] = list(title)

        for idx, item in enumerate(self._items):
            if not (self.scroll_y <= idx < self.scroll_y+self.h-4):
                continue
            item_text = chr(ord('a') + idx) + ') ' + str(item)
            display[2+idx-self.scroll_y][left:left+len(item_text)] = list(item_text)

        if self.scroll_y > 0: # more above
            if len(self._items) > self.scroll_y + self.h-4: # more below
                text = '      -^- more -v-'
            else:
                text = '      -^- more ---'
        elif len(self._items) > self.scroll_y + self.h-4: # more below
            text = '      --- more -v-'
        else:
            text = ''
        display[self.h-2][left:left+len(text)] = list(text)
    
    def recv_key(self, key):
        if self.state == State.DEFAULT:
            if key == 'i':
                self.shown = False
            elif key == 'down':
                self.scroll_y = min(max(0, len(self._items)-self.h+4), self.scroll_y+1)
            elif key == 'up':
                self.scroll_y = max(0, self.scroll_y-1)
            elif key == 'enter':
                self._items.clear()
                self.scroll_y = 0
                self.unit.zone.add_message('Backpack cleared.')
            else:
                self.select(key)
        elif self.state == State.ITEM_SELECTED:
            if self.selected_item is None:
                return
            if key in self.selected_item.actions.keys():
                action = self.selected_item.actions[key]
                if action == 'drop':
                    self.unit.zone.add_message(f'You drop {self.selected_item}.')
                    self.items.remove(self.selected_item)
                    self.selected_item.x, self.selected_item.y = self.unit.x, self.unit.y
                    self.unit.zone.place_item(self.selected_item, False)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'examine':
                    self.unit.zone.add_message(self.selected_item.get_info())
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'equip':
                    self.unit.zone.add_message(f'You equip {self.selected_item}.')
                    self.unit.char_pane.equip(self.selected_item)
                    self.items.remove(self.selected_item)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action in ['eat', 'drink', 'read']:
                    if action == 'eat':
                        self.unit.zone.add_message(f'You eat {self.selected_item}.')
                    elif action == 'drink':
                        self.unit.zone.add_message(f'You drink {self.selected_item}.')
                    elif action == 'read':
                        self.unit.zone.add_message('The written words fade as you read them.')
                    self.selected_item.affect_unit(self.unit, 'used')
                    self.selected_item.quantity -= 1
                    if self.selected_item.destroyed:
                        self.items.remove(self.selected_item)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'spill':
                    self.unit.zone.add_message(f'You spill {self.selected_item} on the ground.')
                    content = self.selected_item.get_content()
                    self.selected_item.quantity = 0
                    content.x, content.y = self.unit.x, self.unit.y
                    self.unit.zone.place_item(content, False)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'throw':
                    self.unit.zone.add_message(f'Throw {self.selected_item} in which direction?')
                    self.state = State.ITEM_USED
            else:
                self.unit.zone.add_message('Action cancelled.')
                self.selected_item = None
                self.state = State.DEFAULT
        elif self.state == State.ITEM_USED:
            if key in ['home', 'up', 'page_up', 'left', 'right', 'end', 'down', 'page_down']:
                action = self.selected_item.actions['t'] # TODO get the actual action
                if action == 'throw':
                    x, y = self.unit.x, self.unit.y
                    self.unit.zone.add_message(f'You throw {self.selected_item}.')
                    self.selected_item.break_('thrown')
                    self.unit.zone.add_message(f'{self.selected_item} shatters as it hits the ground.')
                    for piece in self.selected_item.pieces:
                        piece.x, piece.y = x+get_dir(key)[0]*4, y+get_dir(key)[1]*4
                        self.unit.zone.place_item(piece, False)
                    self.items.remove(self.selected_item)
                    self.selected_item = None
                    self.state = State.DEFAULT
            else:
                self.unit.zone.add_message('Action cancelled.')
                self.selected_item = None
                self.state = State.DEFAULT
    
    def tick(self):
        # TODO take into account unit and zone temperature
        # TODO take into account other items' temperature
        for item in self.items:
            item.update_temperature(self.unit.temperature)

        for item in list(self.items):
            if item.broken:
                pieces = item.pieces
                for piece in pieces:
                    self.items.append(piece)
                self.items.remove(item)

    def select(self, c):
        if c is None or len(c) > 1:
            return
        idx = ord(c) - ord('a')
        if idx >= len(self._items) or not c.isalpha():
            return
        print(self._items, type(self._items[0]))
        item = self._items[idx]
        self.selected_item = item
        if item.actions:
            self.unit.zone.add_message(item.select_text)
            self.state = State.ITEM_SELECTED
    