from .pane import Pane


class CharPane(Pane):
    def __init__(self, unit):
        Pane.__init__(self, 0, 0)
        self.unit = unit
        self.slots = ['head', 'chest', 'hands', 'weapons/shields', 'legs', 'feet']
        self.items = {s:[] for s in self.slots}
        self.shown = False

    def recv_key(self, key):
        if key == 'e':
            self.shown = False
        if key in [str(i) for i in range(1, 6 + 1)]:
            slot = self.slots[int(key)-1]
            for item in self.items[slot]:
                self.unequip(item)
                self.unit.inv.add_item(item)

    # drawing
    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2

        title = 'Character window'
        display[1][left:left+len(title)] = list(title)

        for idx, (slot, items) in enumerate(self.items.items()):
            text = f'{1+idx}: {slot}:'.ljust(8) + repr(items)
            display[2+idx][left:left+len(text)] = list(text)

        stats = ['attack damage', 'running speed', 'armor', 'block', 'cold res']
        for idx, stat in enumerate(stats):
            value = ''
            if stat == 'attack damage':
                value = self.unit.damage
            elif stat == 'armor':
                value = self.unit.armor
            elif stat == 'block':
                value = f'{self.unit.block*10}%'
            elif stat == 'cold res':
                value = self.unit.resistance.cold
            text = f'{stat}:'.rjust(20) + str(value)
            display[2+idx][left+30:left+30+len(text)] = list(text)

        text = 'Press [1-{}] to unequip.'.format(len(self.slots))
        display[self.h-3][left:left+len(text)] = list(text)
        text = 'Press [esc] to close.'
        display[self.h-2][left:left+len(text)] = list(text)
            
    def equip(self, item):
        # self.world.log.add_message(f'You equip {item}.')
        self.items[item.slot].append(item)
        for mod in item.modifiers:
            self.unit.modifiers.append(mod)

    def unequip(self, item):
        # self.world.log.add_message(f'You unequip {item}.')
        self.items[item.slot].remove(item)
        for mod in item.modifiers:
            self.unit.modifiers.remove(mod)

    def get_items_at_slot(self, slot):
        return self.items[slot]
            