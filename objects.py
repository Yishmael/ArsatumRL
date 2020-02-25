import random
from collections import defaultdict

from utils import sign, distance_between_points, get_direction, WIDTH, HEIGHT, get_icon, within_bounds, distance_between
from gui.inventory import Inventory
from gui.charpane import CharPane
from item import Item

class GameObject:
    def __init__(self, zone, name, x, y, items=[]):
        self.zone = zone
        self.name = name
        self.icon = get_icon(self.name)
        self.x = x
        self.y = y
        self.just_moved = True
        self.temperature = 20
        self.inv = Inventory(self, items)
        self._events = []

    # def __repr__(self):
    #     return self.icon

    def __str__(self):
        return self.name
            
    def sees(self, o):
        return True or self.x == o.x or self.y == o.y

    def walkable(self, tile):
        return tile in ['.']

    def has_just_moved(self):
        just_moved = self.just_moved
        self.just_moved = False
        return just_moved

    def can_move_to(self, x, y):
        if not within_bounds(x, y):
            return False
        tile = self.zone.get_tile_at(x, y)
        if not self.walkable(tile):
            if tile == '#':
                if self.icon == '@':
                    pass #'You flatten yourself against the wall'
            elif tile == '_':
                self.inv.recv('refill water')
            return False
        for u in self.zone.units:
            if u is self:
                continue
            if (u.x, u.y) == (x, y):
                return False
        return True
    
    def get_events(self):
        events = list(self._events)
        self._events.clear()
        return events
       
    # TODO use the formula with equilibrium
    # TODO take clothes worn into account
    def update_temperature(self, ambient_temperature):
        self.temperature += (ambient_temperature - self.temperature) * 0.0001
        for item in self.inv.items:
            item.update_temperature(self.temperature)
            

class Creature(GameObject):
    def __init__(self, zone, name, x, y, items):
        super(Creature, self).__init__(zone, name, x, y, items)
        self.org_x = x
        self.org_y = y
        self.exp = 0
        self._base_armor = 0
        self._base_block = 0
        self.temperature = 37
        self.resistance = Resistance()
        self._statuses = {}
        self._stamina = 100
        self._food = 5
        self._water = 5
        self.modifiers = []
        self._base_damage = 0
        self.char_pane = CharPane(self)
        if self.icon == '@':
            self._hp = 30
            self._base_damage = 1
            self.exp_reward = 0
        elif self.name == 'white rat':
            self._hp = 2
            self.vision_distance = 3
            self._base_damage = 1
            self.exp_reward = 1
        elif self.name == 'coyote':
            self._hp = 3
            self.vision_distance = 4
            self._base_damage = 2
            self.exp_reward = 3
        elif self.name == 'cave bat':
            self._hp = 2
            self.vision_distance = 8
            self._base_damage = 1
            self.exp_reward = 1
        else:
            self._hp = 10

    def move_idle(self):
        if random.random() < 0.90:
            return
        if distance_between_points((self.x, self.y), (self.org_x, self.org_y)) < 2:
            self.move_delta(random.randint(-1, 1), random.randint(-1, 1))
        else:
            direction = get_direction((self.x, self.y), (self.org_x, self.org_y))
            self.move_delta(direction.x, direction.y)

    def move_toward_point(self, x, y):
        dx, dy = get_direction((self.x, self.y), (x, y))
        self.move_delta(dx, dy)
    
    def move_toward_object(self, o):
        dx, dy = get_direction((self.x, self.y), (o.x, o.y))
        self.move_delta(dx, dy)
    
    def move_delta(self, dx, dy):
        if self.can_move_to(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            self.just_moved = True
            self.stamina -= self.inv.mass / 50
        else:
            self.interact_with(self.x + dx, self.y + dy)

    def interact_with(self, x, y):
        for u in self.zone.units:
            if (u.x, u.y) == (x, y):
                # preventing units from attacking each other
                if '@' in [self.icon, u.icon]:
                    self.attack(u)
                break
        if not within_bounds(x, y):
            return
        tile = self.zone.get_tile_at(x, y)

        if self.icon == '@' and tile.isdigit():
            self.show_shop = True

    def tick(self):
        # self.temperature += (37 - self.temperature) * 0.01
        if 'poisoned' in self.statuses:
            self.food -= 0.1 * (1 - self.resistance.poison)
            self.water -= 0.2 * (1 - self.resistance.poison)
        if 'bleeding' in self.statuses:
            self.hp -= 0.1 + self.statuses['bleeding']/100
        self.stamina += 0.1
        for status, duration in list(self.statuses.items()):
            self.statuses[status] -= 1
            if duration <= 0:
                del self.statuses[status]

        if self.icon != '@':
            if distance_between(self, self.zone.player) <= self.vision_distance and \
                    self.sees(self.zone.player):
                self.move_toward_object(self.zone.player)
                if random.random() < 0.05:
                    self.move_delta(random.randint(-1, 1), random.randint(-1, 1))
            else:
                pass # self.move_idle()     
            
    def attack(self, u):
        blocked = random.random() < u.block/10
        if self.icon == '@':
            if blocked:
                self.zone.add_message(f'{u} blocks your attack.')
            else:
                u.hp -= self.damage
                hands_items = self.char_pane.get_items_at_slot('weapons/shields')
                if len(hands_items) > 0:
                    self.zone.add_message(f'You hit {u} with {random.choice(hands_items)}.')
                else:
                    self.zone.add_message(f'You punch {u}.')
        elif u.icon == '@':
            if blocked:
                self.zone.add_message(f'You block {self}\'s attack.')
            else:
                u.hp -= self.damage
                self.zone.add_message(f'{self} scratches you.')
                if self.icon == 'C':
                    if random.random() < 1.1:
                        u.add_status('bleeding')
        if u.hp <= 0:
            self.exp += u.exp_reward
        self.stamina -= 1

    def pickup(self):
        for item in list(self.zone.items):
            if (item.x, item.y) == (self.x, self.y):
                if not item.collectable():
                    continue
                self.zone.items.remove(item)
                self.inv.add_item(item)
                if self.icon == '@':
                    self.zone.add_message(f'You pick up {item}.')
                else:
                    self.zone.add_message(f'{self} picks up {item}.')

    @property
    def dead(self):
        return self._hp <= 0

    # TODO recompute these only when a mod is added or removed 
    @property
    def damage(self):
        total = self._base_damage
        for mod in self.modifiers:
            stat, delta = mod.split()
            delta = int(delta)
            if stat == 'damage':
                total += delta
        return total
    
    @property
    def armor(self):
        total = self._base_armor
        for mod in self.modifiers:
            stat, delta = mod.split()
            delta = int(delta)
            if stat == 'armor':
                total += delta
        return total

    @property
    def block(self):
        total = self._base_block
        for mod in self.modifiers:
            stat, delta = mod.split()
            delta = int(delta)
            if stat == 'block':
                total += delta
        return total
        
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)
        if self._hp == 0:
            self._events.append('dead')

    @property
    def stamina(self):
        return self._stamina
    
    @stamina.setter
    def stamina(self, value):
        self._stamina = min(100, max(0, value))
        self.statuses.pop('tired', None)
        self.statuses.pop('exhausted', None)
        if self._stamina in range(10, 15):
            self.add_status('tired')
        elif self._stamina < 2: # NOTE should be 0, but regen happens too soon
            self.add_status('exhausted')
    
    @property
    def water(self):
        return self._water

    @water.setter
    def water(self, value):
        self._water = min(100, max(0, value))
        self.statuses.pop('thirsty', None)
        self.statuses.pop('dehydrated', None)
        if self._water in range(10, 20):
            self.add_status('thirsty')
        elif self._water in range(0, 10):
            self.add_status('dehydrated')

    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        self._food = min(100, max(0, value))
        self.statuses.pop('hungry', None)
        self.statuses.pop('starving', None)
        if self._food in range(10, 20):
            self.add_status('hungry')
        elif self._food in range(0, 10):
            self.add_status('starving')
    
    @property
    def statuses(self):
        return self._statuses
    
    def add_status(self, status):
        self._statuses[status] = 1
        if status == 'poisoned':
            # setting duration
            self._statuses[status] = 100
        elif status == 'bleeding':
            # setting duration
            self._statuses[status] = 50
        else: #HACK making these not expire
            self._statuses[status] = 99999

class Resistance:
    def __init__(self):
        self.cold = 0
        self.fire = 0
        self.poison = 0