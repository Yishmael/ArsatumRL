import os
import sys
import time
import random

import curses

from console import Console
from objects import GameObject, Creature
from utils import sign, distance_between, distance_between_points, apply_fov, clear
from gui.shop import Shop
from gui.charpane import CharPane
from gui.journal import Journal
from gui.log import Log
from item import Item 
from generators.snailgen import SnailGen
from generators.zone import Zone
from generators.worldgenerator import WorldGenerator

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.console = None
        # self.console = Console()
        self.show_inv = False
        self.shop = Shop(self)
        self.char_pane = CharPane(self)
        self.show_shop = False
        self.show_char_pane = False
        self.journal = Journal(self)
        self.show_journal = False
        self.log = Log(self)
        self.show_log = False
        self.display = None
        self.turn_count = 0
        self.ground_items = []

    def init(self):
        worldgen = WorldGenerator(self.width, self.height)
        worldgen.generate_world()
        self.zones = worldgen.zones
        self.zone_id = 0
        self.zone = self.zones[self.zone_id]
        for zone_id in range(len(self.zones)): 
            for unit in list(self.zones[zone_id].units):
                if type(unit) is tuple: #NOTE temp
                    name, x, y = unit
                    self.zones[zone_id].units.remove(unit)
                    self.spawn(name, x, y, zone_id, [])
            for item in list(self.zones[zone_id].items):
                if type(item) is tuple: #NOTE temp
                    name, x, y = item
                    self.zones[zone_id].items.remove(item)
                    self.place(name, x, y, zone_id)
        self.player = Creature(self, 'You', 15, 5, 0,
                [Item(i) for i in ['unlit torch', 'green potion', 'scroll of alchemy']])
        self.zone.units.append(self.player)

    def spawn(self, name, x, y, zone_id=None, items=[]):
         # TODO always pass in Creature, not its name
        if zone_id is None:
            zone_id = self.zone_id
        self.zones[zone_id].units.append(Creature(self, name, x, y, zone_id, items))

    def place(self, name, x, y, zone_id=None):
        if zone_id is None:
            zone_id = self.zone_id
        if type(name) is Item: # TODO always pass in Item, not its name
            item = name
            name = item.name
        else:
            item = Item(name)
        self.zones[zone_id].items.append(GameObject(self, name, x, y, zone_id, [item]))

    def tick(self):
        self.ground_items = []
        for o in self.zone.items:
            if (o.x, o.y) == (self.player.x, self.player.y):
                self.ground_items.extend(o.inv.items)
        for item1 in list(self.ground_items): # poisoning the food
            if 'green puddle' in item1.name:
                for item2 in list(self.ground_items):
                    if 'meal' in item2.name:
                        item2.poisonous = True
                        # TODO fix being able to pick up unpoisoned food after spilling poison on it 
                        # and immediately picking it up
                        self.ground_items.remove(item1)
        
        for u in list(self.zone.units):
            u.update_temperature(self.zone.temperature)
            if 'poisoned' in u.statuses:
                u.hp -= 0.1 * (1 - u.resistance.poison)
            u.stamina += 0.1
            for status, duration in list(u.statuses.items()):
                # self.log.add_message(f'{status}: {duration}')
                u.statuses[status] -= 1
                if duration <= 0:
                    del u.statuses[status]
            if u.hp <= 0:
                self.zone.units.remove(u)
                if u.icon == '@':
                    self.log.add_message('You die.')
                else:
                    self.log.add_message(f'{u} dies.')
                for item in u.inv.items:
                    self.place(item, u.x, u.y)
                continue
            if u.icon != '@':
                if distance_between(u, self.player) <= u.vision_distance and \
                        u.sees(self.player):
                    u.move_toward_object(self.player)
                    if random.random() < 0.05:
                        u.move_delta(random.randint(-1, 1), random.randint(-1, 1))
                else:
                    pass #u.move_idle()
        for item in list(self.zone.items):
            item.update_temperature(self.zone.temperature)

    def draw(self):
        self.display = list(list(row) for row in self.zone.get_grid())
        for o in self.zone.items:
            if o.icon:
                self.display[o.y][o.x] = o.icon
        for u in self.zone.units:
            if u.icon:
                self.display[u.y][u.x] = u.icon
        # apply_fov(self.player, self.display, 3)
        if self.show_inv:
            self.player.inv.apply_on(self.display)
        elif self.show_shop:
            self.shop.apply_on(self.display)
        elif self.show_char_pane:
            self.char_pane.apply_on(self.display)
        elif self.show_journal:
            self.journal.apply_on(self.display)
        elif self.show_log:
            self.log.apply_on(self.display)

        #curses
        if self.console:
            self.console.update_display(self.display)
        else:
            print('\n'.join(''.join(row) for row in self.display))
        with open('display.txt', 'w') as f:
            f.write('\n'.join(''.join(row) for row in self.display))

        if self.ground_items and self.player.has_just_moved():
            self.log.add_message(f'You see {self.ground_items} at your feet.')
        if self.zone.get_tile_at(self.player.x, self.player.y) == '>':
            self.log.add_message(f'You see stairs leading down.')
        if self.zone.get_tile_at(self.player.x, self.player.y) == '<':
            self.log.add_message(f'You see stairs leading up.')

        print(self.log.get_last_message())
        print(', '.join([f'HP:{self.player.hp:.0f}', f'XP:{self.player.exp}', 
                        f'STA:{self.player.stamina:.0f}', 
                        # f'TEM:{self.player.temperature:.1f}°C',
                        f'WATER:{self.player.water}', f'FOOD:{self.player.food}',
                        # f'ZONE:{self.zone.temperature}°C',
                        f'T:{self.turn_count}']))
                
        print(f', '.join(self.player.statuses))

    def set_zone_id(self, index):
        self.zone.units.remove(self.player)
        self.zone_id = index
        self.zone = self.zones[self.zone_id]
        self.zone.units.append(self.player)

    def change_zone(self):
        for staircase in self.zone.staircases:
            loc = staircase.get_exit_location(self.player.x, self.player.y, self.zone_id)
            if not loc:
                continue
            x, y, zone_id = loc
            if zone_id is not None:
                if zone_id > self.zone_id:
                    self.log.add_message(staircase.get_descend_message())
                else:
                    self.log.add_message(staircase.get_ascend_message())
                self.set_zone_id(zone_id)
                self.player.x, self.player.y = x, y
                break
    def get_items_in_range(self, x, y, distance):
        items = []
        for o in self.zone.items:
            if distance_between_points((x, y), (o.x, o.y)) <= distance:
                for item in o.inv.items:
                    items.append(item)
        return items


    def update(self, advance_turn):
        if advance_turn:
            self.turn_count += 1
        clear()
        if advance_turn:
            self.tick()
        self.draw()
        self.log.hide_last_message()
