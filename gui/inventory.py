import random

from .pane import Pane
from utils import get_dir
from item import Item

class State:
    DEFAULT = 0
    ITEM_SELECTED = 1
    ITEM_USED = 2

class Inventory(Pane):
    def __init__(self, world, items=[]):
        super(Inventory, self).__init__(32, 8)
        self._items = list(items)
        self.world = world
        self.state = State.DEFAULT
        self.selected_item = None
        self.scroll_y = 0

    def __repr__(self):
        return ', '.join(item.name for item in self._items)

    def remove_item(self, item):
        if item not in self._items:
            raise ValueError(f'{item} can\'t be removed.')
        self._items.remove(item)

    def add_item(self, item):
        self.world.log.add_message(f'You pick up {item}.')
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
                    self.world.log.add_message(f'You fill {name} with {value}.')
                    break
            else:
                self.world.log.add_message('You wash your face in the fountain.')
    
    @property
    def items(self):
        return self._items

    @property
    def mass(self):
        return sum((item.mass for item in self._items))

    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2

        total_mass = sum(item.mass for item in self._items)
        title = f'Backpack ({total_mass:.1f} kg)'
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
                self.world.show_inv = False
            elif key == 'down':
                self.scroll_y = min(max(0, len(self._items)-self.h+4), self.scroll_y+1)
            elif key == 'up':
                self.scroll_y = max(0, self.scroll_y-1)
            elif key == 'enter':
                self._items.clear()
                self.world.log.add_message('Backpack cleared.')
            else:
                self.select(key)
        elif self.state == State.ITEM_SELECTED:
            if self.selected_item is None:
                return
            if key in self.selected_item.actions.keys():
                action = self.selected_item.actions[key]
                if action == 'drop':
                    self.world.log.add_message(f'You drop {self.selected_item}.')
                    self._items.remove(self.selected_item)
                    x, y = self.world.player.x, self.world.player.y
                    self.world.place(self.selected_item, x, y)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'spill':
                    self.world.log.add_message(f'You spill {self.selected_item} on the ground.')
                    content = self.selected_item.get_content()
                    self.selected_item.quantity = 0
                    x, y = self.world.player.x, self.world.player.y
                    self.world.place(content, x, y)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'examine':
                    self.world.log.add_message(self.selected_item.get_info())
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'equip':
                    self.world.log.add_message(f'You equip {self.selected_item}.')
                    self.world.char_pane.equip(self.selected_item)
                    self._items.remove(self.selected_item)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'eat':
                    self.world.log.add_message(f'You eat {self.selected_item}.')
                    self.selected_item.affect(self.world.player)
                    self._items.remove(self.selected_item)
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'drink':
                    self.world.log.add_message(f'You drink {self.selected_item}.')
                    self.selected_item.affect(self.world.player)
                    self.selected_item.quantity -= 1
                    self.selected_item = None
                    self.state = State.DEFAULT
                elif action == 'throw':
                    self.world.log.add_message(f'Throw {self.selected_item} in which direction?')
                    self.state = State.ITEM_USED
                elif action == 'read': # TODO combine read and drink and eat
                    self.world.log.add_message('The written words fade as you read them.')
                    self.selected_item.affect(self.world.player)
                    self.selected_item.quantity -= 1
                    self.selected_item = None
                    self.state = State.DEFAULT
            else:
                self.world.log.add_message('Action cancelled.')
                self.selected_item = None
                self.state = State.DEFAULT
        elif self.state == State.ITEM_USED:
            if key in ['up', 'left', 'down', 'right']:
                action = self.selected_item.actions['t'] # TODO get the actual action
                if action == 'throw':
                    self._items.remove(self.selected_item)
                    x, y = self.world.player.x, self.world.player.y
                    self.world.log.add_message(f'You throw {self.selected_item}.')
                    # TODO update the item instead of spawning new
                    # and display a message that item broke
                    # call method to break the item, making it contain the pieces
                    for item in self.selected_item.get_broken():
                        self.world.place(item, x+get_dir(key)[0]*4, y+get_dir(key)[1]*4)
                    self.selected_item = None
                    self.state = State.DEFAULT
            else:
                self.world.log.add_message('Action cancelled.')
                self.selected_item = None
                self.state = State.DEFAULT

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
            self.world.log.add_message(item.select_text)
            self.state = State.ITEM_SELECTED
    