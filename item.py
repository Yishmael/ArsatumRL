
import random
from utils import get_icon

class Item:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.mass = 0
        self.poisonous = False
        self._temperature = 15
        self.icon = get_icon(self.name)
        self.slot = ''
        self.broken = False
        self.destroyed = False
        if 'potion' in name: 
            self.mass = 0.8
            self._quantity = 3
            if 'green potion' in name:
                self.poisonous = True
        elif 'green puddle' in name:
            self._quantity = 3
        elif 'poison cloud' in name:
            self._duration = 10
        elif 'flask' in name:
            self.mass = 0.2
            self._quantity = 0
        elif 'scroll' in name:
            self._quantity = 0
            if 'blank scroll' not in name:
                self._quantity = 1
        elif 'meal' in name:
            self.mass = 0.1
            self._quantity = 1
        elif 'sweater' in name:
            self.mass = 1
            self.slot = 'chest'
        elif 'barrel top' in name:
            self.mass = 3
            self.slot = 'weapons/shields'
        elif 'stick' in name:
            self.mass = 0.3
            self.slot = 'weapons/shields'
        elif 'torch' in name:
            self.mass = 0.3
            self._duration = 50
            self.slot = 'weapons/shields'
        elif 'boots' in name:
            self.mass = 0.7
            self.slot = 'feet'

    def __repr__(self):
        s = ''
        if 'potion' in self.name:
            s += f'{self.name} (qty:{self.quantity})'
        elif 'torch' in self.name:
            s += f'{self.name} (dur:{self.duration})'
        elif self.mass != 0:
            s += f'{self.name} ({self.mass}kg)'
        else:
            s += f'{self.name}'
        # s += f' ({self.temperature:.1f})°C'
        return s

    def update_temperature(self, ambient_temperature):
        self.temperature += (ambient_temperature - self.temperature) * 0.01
    
    def tick(self):
        self.duration -= 1

    @property
    def select_text(self):
        return f'What to do with {self.name}? ' + str(self.actions)

    @property
    def modifiers(self):
        modifiers = []
        if 'sweater' in self.name:
            modifiers.append('armor +1')
        elif 'barrel top' in self.name:
            modifiers.append('block +1')
        elif 'torch' in self.name:
            if self.name == 'lit torch':
                modifiers.append('damage +1')
                modifiers.append('vision +5')
        return modifiers

    @property
    def actions(self):
        actions = {'d': 'drop', 'x': 'examine'}
        if 'sweater' in self.name or 'stick' in self.name or 'barrel top' in self.name or \
            'torch' in self.name or 'boots' in self.name:
            actions.update({'e': 'equip'})
        elif 'meal' in self.name and 'frozen' not in self.name:
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
    def duration(self):
        if '_duration' not in dir(self):
            return 0
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = max(0, value)
        if self._duration == 0:
            if self.name == 'lit torch':
                # TODO update user's stars if item changes while equipped
                self.name = 'unlit torch'
            elif self.name == 'poison cloud':
                self.destroyed = True

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = min(10, max(0, value))
        if 'potion' in self.name:
            self.mass = 0.2 + self._quantity * 0.2
        if self._quantity == 0:
            if 'potion' in self.name:
                self.name = 'glass flask'
            elif 'scroll' in self.name:
                self.name = 'blank scroll'
            elif 'meal' in self.name:
                self.destroyed = True
            elif 'green puddle' in self.name:
                self.destroyed = True
            elif self.name == 'poison cloud':
                self.destroyed = True
    
    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        if 'potion' in self.name:
            if self.quantity == 3 and self.temperature < -1:
                self.break_('frozen')
        elif 'meal' in self.name:
            if self.temperature < -1:
                self.name = 'frozen meal'            
            if self.temperature > 0:
                self.name = 'hearty meal'
        elif 'puddle' in self.name and 'frozen' not in self.name:
            if self.temperature < -1:
                self.name = 'frozen ' + self.name
            if self.temperature > 0:
                self.name  = self.name.replace('frozen ', '')
                
    def get_info(self):
        return Item.info(self.name)

    #TODO settle the order of messages and make it more generic
    def affect_unit(self, unit, event_type):
        if event_type == 'used':
            if 'potion' in self.name:
                if 'yellow' in self.name:
                    unit.hp += 3
                    unit.zone.add_message('You feel better.')
                    return
                if 'amber' in self.name:
                    unit.resistance.cold = 100
                    unit.zone.add_message('You feel much warmer.')
                    return
                if 'green' in self.name:
                    unit.zone.add_message('It tastes very sweet.')
                    unit.add_status('poisoned')
                    return
                if 'water' in self.name:
                    unit.hp += 0.5
                    unit.water += 10
                    unit.zone.add_message('You feel refreshed.')
                    return
            elif 'meal' in self.name:
                if self.poisonous:
                    unit.food += 2
                    unit.zone.add_message('It tastes sweeter than expected.')
                    unit.add_status('poisoned')
                    return
                else:
                    unit.food += 10
                    unit.zone.add_message('It\'s chewy, but tastes great.')
                    return
            elif 'scroll' in self.name:
                if 'alchemy' in self.name:
                    items = unit.zone.get_items_in_range(unit.x, unit.y, 1)
                    for item in items:
                        if 'water potion' in item.name:
                            qty = item.quantity
                            item.quantity = 0
                            item.fill('amber', qty)
        elif event_type == 'stepped':
            if self.name == 'glass shard':    
                if unit.char_pane.get_items_at_slot('feet'):
                    if unit.icon == '@':
                        unit.zone.add_message('You hear glass shatter under your weight.')
                        self.destroyed = True
                else:
                    if unit.icon == '@':
                        unit.zone.add_message('You cut your foot on a glass shard.')
                    else:
                        unit.zone.add_message(f'{unit} cuts its foot on glass shards.')
                    unit.hp -= 2
            elif self.name == 'stick':
                unit.zone.add_message('You step on a dry stick, snapping it in half.')
                unit.zone.emit_sound(unit.x, unit.y, 50)
                self.destroyed = True
            elif self.name == 'poison cloud':
                unit.hp -= 1


    def affect_item(self, item):
        if item is self or self.destroyed or item.destroyed:
            return
        if 'green puddle' in self.name and 'frozen' not in self.name:
            if 'meal' in item.name:
                item.poisonous = True
        if 'puddle' in self.name and 'frozen' not in self.name:
            if 'puddle' in item.name and 'frozen' not in item.name:
                item.destroyed = True
                        
    def get_content(self):
        if 'potion' in self.name:
            item = Item(self.name.split()[0] + ' puddle')
            item.temperature = self.temperature
            return item
        return None

    def break_(self, cause):
        if self.broken:
            return
        self.broken = True
        self.pieces = []
        # TODO create sound
        if cause == 'frozen': # only potions can do this
            item = Item('glass shard')
            item.temperature = self.temperature
            self.pieces.append(item)
            item = Item(self.name.split()[0] + ' ice')
            item.temperature = self.temperature
            self.pieces.append(item)
        elif cause == 'thrown':
            if 'flask' in self.name or 'potion' in self.name:
                if random.random() < 1.1:
                    item = Item('glass shard')
                    item.temperature = self.temperature
                    self.pieces.append(item)
                content = self.get_content()
                if content:
                    self.pieces.append(content)
        
    @property
    def collectable(self):
        return 'puddle' not in self.name and 'poison cloud' not in self.name

    def fill(self, liquid, quantity=3):
        # don't replace liquid if item it already contains a different one
        if 'flask' not in self.name and f'{liquid} potion' not in self.name:
            return
        if liquid == 'water':
            self.name = 'water potion'
            self.mass = 0.5
            self.quantity = quantity
        if liquid == 'amber':
            self.name = 'amber potion'
            self.mass = 0.5
            self.quantity = quantity

    def full(self):
        return self.quantity >= 3

    def refillable(self):
        return 'water potion' in self.name or 'flask' in self.name

    @staticmethod
    def info(name):
        details = {
            'glass flask': 'this {} can be used to store liquids.',
            'scroll of alchemy': '{} transmutes nearby water to a random liquid.',
            'water potion': 'A bottle of water. Use with caution.'
        }
        if name in details.keys():
            return details[name].format(name)
        else:
            return f'Not much is known about this {name}.'
