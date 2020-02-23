
import random
#CHANGE!!
from utils import get_icon

class Item:
    def __init__(self, name):
        self.name = name
        self.mass = 0
        self.poisonous = False
        self.temperature = 10
        self.icon = get_icon(self.name)
        self.modifiers = []
        self.slot = ''
        if 'potion' in name: 
            self.mass = 0.5
            self._quantity = 3
            if 'green potion' in name:
                self.poisonous = True
        elif 'flask' in name:
            self.mass = 0.2
            self._quantity = 0
        elif 'scroll' in name:
            self._quantity = 0
            if 'blank scroll' not in name:
                self._quantity = 1
        elif 'meal' in name:
            self.mass = 0.1
        elif 'sweater' in name:
            self.mass = 1
            self.modifiers.append('armor +1')
            self.slot = 'chest'
        elif 'barrel top' in name:
            self.mass = 3
            self.modifiers.append('block +1')
            self.slot = 'weapons/shields'
        elif 'stick' in name:
            self.mass = 0.3
            self.slot = 'weapons/shields'
        elif 'glass shard' in name:
            self.icon = ''
        elif 'torch' in name:
            self.mass = 0.3
            self._duration = 360
            self.modifiers.append('damage +1')
            self.slot = 'weapons/shields'

    def __repr__(self):
        s = ''
        if 'potion' in self.name:
            s += f'{self.name} (qty:{self._quantity}) '
        elif 'torch' in self.name:
            s += f'{self.name} (dur:{self._duration}) '
        elif self.mass != 0:
            s += f'{self.name} ({self.mass}kg) '
        else:
            s += f'{self.name} '
        s += f'({self.temperature:.1f})°C'
        
        return s

    @property
    def select_text(self):
        return f'What to do with {self.name}? ' + str(self.actions)

    @property
    def actions(self):
        actions = {'d': 'drop', 'x': 'examine'}
        if 'sweater' in self.name or 'stick' in self.name or 'barrel top' in self.name or \
            'torch' in self.name:
            actions.update({'e': 'equip'})
        elif 'meal' in self.name:
            actions.update({'e': 'eat'})
        elif 'pebble' in self.name:
            actions.update({'t': 'throw'})
        elif 'scroll' in self.name:
            if 'blank' not in self.name:
                actions.update({'e': 'read'})
        elif 'flask' in self.name:
            actions.update({'t': 'throw'})
        elif 'potion' in self.name:
            actions.update({'e': 'drink', 's': 'spill', 't': 'throw'})
        return actions

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = min(3, max(0, value))
        if self._quantity == 0:
            if 'potion' in self.name:
                self.name = 'glass flask'
            elif 'scroll' in self.name:
                self.name = 'blank scroll'
                
    def get_info(self):
        return f'Not much is known about this {self.name}.'
    
    #TODO settle the order of messages and make it more generic
    def affect(self, unit):
        if 'potion' in self.name:
            if 'yellow' in self.name:
                unit.hp += 3
                unit.world.log.add_message('You feel better.')
                return
            if 'amber' in self.name:
                unit.resistance.cold = 100
                unit.world.log.add_message('You feel much warmer.')
                return
            if 'green' in self.name:
                unit.world.log.add_message('It tastes very sweet.')
                unit.add_status('poisoned')
                return
            if 'water' in self.name:
                unit.hp += 0.5
                unit.water += 10
                unit.world.log.add_message('You feel refreshed.')
                return
        elif 'meal' in self.name:
            if self.poisonous:
                unit.food += 2
                unit.world.log.add_message('It tastes sweeter than expected.')
                unit.add_status('poisoned')
                return
            else:
                unit.food += 10
                unit.world.log.add_message('It\'s chewy, but tastes great.')
                return
        elif 'scroll' in self.name:
            if 'alchemy' in self.name:
                items = unit.world.get_items_in_range(unit.x, unit.y, 1)
                for item in items:
                    if 'water potion' in item.name:
                        qty = item.quantity
                        item.quantity = 0
                        item.fill('amber', qty)
                        
    def get_content(self):
        if 'potion' in self.name:
            return Item(self.name.split(maxsplit=1)[1] + ' puddle')
        return None

    def get_broken(self):
        res = []
        if 'flask' in self.name or 'potion' in self.name:
            if random.random() < 1.1:
                res.append(Item('glass shard'))
            content = self.get_content()
            if content:
                res.append(content)
        return res
        
    def collectable(self):
        return 'puddle' not in self.name

    def fill(self, liquid, quantity=3):
        # don't replace liquid if item it already contains a different one
        if 'flask' not in self.name and f'{liquid} potion' not in self.name:
            return
        if liquid == 'water':
            self.name = 'water potion'
            self.mass = 0.5
            self._quantity = quantity
        if liquid == 'amber':
            self.name = 'amber potion'
            self.mass = 0.5
            self._quantity = quantity

    def full(self):
        return self._quantity >= 3

    def refillable(self):
        return 'water potion' in self.name or 'flask' in self.name
