from .pane import Pane
from item import Item

class Shop(Pane):
    def __init__(self, world):
        Pane.__init__(self, 0, 0)
        self.items = [Item(i) for i in ['amber potion', 'yellow potion', 'green potion', 'green potion']]
        self.world = world

    def __repr__(self):
        return ', '.join(item.name for item in self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def recv_key(self, key):
        self.buy(key)

    def add_item(self, item):
        self.items.append(item)

    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2
        top = 3
        title = 'Miscellaneous'
        owner = 'Hanil Birdcatcher'
        total = F'{title} shop run by {owner}'
        display[1][left:left+len(total)] = list(total)

        for idx, item in enumerate(self.items):
            char = chr(ord('a') + idx)
            item_text = char + ') ' + item.name
            display[1+top+idx][left:left+len(item_text)] = list(item_text)
        if len(self.items) > 0:
            text = f'Press [a-{char}] to buy.'
            display[self.h-2][left:left+len(text)] = list(text)
        
    def buy(self, c):
        if c is None or len(c) > 1:
            return
        idx = ord(c) - ord('a')
        if idx >= len(self.items) or not c.isalpha():
            return
        self.world.log.add_message(f'You buy {self.items[idx]}.')
        self.world.player.inv.add_item(self.items[idx])
        del self.items[idx]
    